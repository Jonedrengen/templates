// Rust Web Server Template using Actix-web
//
// Template for creating a REST API server with Actix-web framework.
//
// Dependencies required in Cargo.toml:
// [dependencies]
// actix-web = "4"
// serde = { version = "1.0", features = ["derive"] }
// serde_json = "1.0"
// uuid = { version = "1.0", features = ["v4"] }
// chrono = { version = "0.4", features = ["serde"] }

use actix_web::{web, App, HttpResponse, HttpServer, Responder, Result};
use chrono::Utc;
use serde::{Deserialize, Serialize};
use std::sync::Mutex;
use uuid::Uuid;

/// Entity data structure
#[derive(Debug, Serialize, Deserialize, Clone)]
struct Entity {
    id: String,
    name: String,
    created_at: String,
}

/// Request payload for creating entities
#[derive(Debug, Deserialize)]
struct CreateEntityRequest {
    name: String,
}

/// Application state
struct AppState {
    entities: Mutex<Vec<Entity>>,
}

/// Home route handler
async fn index() -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({
        "message": "Welcome to the API",
        "version": "1.0.0"
    }))
}

/// Health check handler
async fn health() -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({
        "status": "healthy",
        "timestamp": Utc::now().to_rfc3339()
    }))
}

/// Get all entities
async fn get_entities(data: web::Data<AppState>) -> Result<impl Responder> {
    let entities = data.entities.lock().unwrap();
    Ok(HttpResponse::Ok().json(&*entities))
}

/// Get entity by ID
async fn get_entity(
    path: web::Path<String>,
    data: web::Data<AppState>,
) -> Result<impl Responder> {
    let id = path.into_inner();
    let entities = data.entities.lock().unwrap();
    
    match entities.iter().find(|e| e.id == id) {
        Some(entity) => Ok(HttpResponse::Ok().json(entity)),
        None => Ok(HttpResponse::NotFound().json(serde_json::json!({
            "error": "Entity not found"
        }))),
    }
}

/// Create a new entity
async fn create_entity(
    payload: web::Json<CreateEntityRequest>,
    data: web::Data<AppState>,
) -> Result<impl Responder> {
    let mut entities = data.entities.lock().unwrap();
    
    let entity = Entity {
        id: Uuid::new_v4().to_string(),
        name: payload.name.clone(),
        created_at: Utc::now().to_rfc3339(),
    };
    
    entities.push(entity.clone());
    
    Ok(HttpResponse::Created().json(entity))
}

/// Delete an entity
async fn delete_entity(
    path: web::Path<String>,
    data: web::Data<AppState>,
) -> Result<impl Responder> {
    let id = path.into_inner();
    let mut entities = data.entities.lock().unwrap();
    
    let initial_len = entities.len();
    entities.retain(|e| e.id != id);
    
    if entities.len() < initial_len {
        Ok(HttpResponse::NoContent().finish())
    } else {
        Ok(HttpResponse::NotFound().json(serde_json::json!({
            "error": "Entity not found"
        })))
    }
}

/// Configure routes
fn configure_routes(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::scope("/api")
            .route("/health", web::get().to(health))
            .route("/entities", web::get().to(get_entities))
            .route("/entities", web::post().to(create_entity))
            .route("/entities/{id}", web::get().to(get_entity))
            .route("/entities/{id}", web::delete().to(delete_entity)),
    );
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Initialize application state
    let app_state = web::Data::new(AppState {
        entities: Mutex::new(Vec::new()),
    });

    println!("Server starting on http://127.0.0.1:8080");

    // Start HTTP server
    HttpServer::new(move || {
        App::new()
            .app_data(app_state.clone())
            .route("/", web::get().to(index))
            .configure(configure_routes)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
