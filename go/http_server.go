package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

// Response represents a standard API response
type Response struct {
	Message string      `json:"message"`
	Data    interface{} `json:"data,omitempty"`
	Status  int         `json:"status"`
}

// Entity represents a basic data entity
type Entity struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// Handler for the home route
func homeHandler(w http.ResponseWriter, r *http.Request) {
	response := Response{
		Message: "Welcome to the API",
		Status:  200,
	}
	sendJSONResponse(w, http.StatusOK, response)
}

// Handler for health check
func healthHandler(w http.ResponseWriter, r *http.Request) {
	response := Response{
		Message: "Service is healthy",
		Status:  200,
		Data: map[string]string{
			"timestamp": time.Now().Format(time.RFC3339),
		},
	}
	sendJSONResponse(w, http.StatusOK, response)
}

// Handler for getting data
func getDataHandler(w http.ResponseWriter, r *http.Request) {
	// Example data
	entities := []Entity{
		{ID: "1", Name: "Entity 1", CreatedAt: time.Now(), UpdatedAt: time.Now()},
		{ID: "2", Name: "Entity 2", CreatedAt: time.Now(), UpdatedAt: time.Now()},
	}

	response := Response{
		Message: "Data retrieved successfully",
		Data:    entities,
		Status:  200,
	}
	sendJSONResponse(w, http.StatusOK, response)
}

// Handler for creating data
func createDataHandler(w http.ResponseWriter, r *http.Request) {
	var entity Entity
	err := json.NewDecoder(r.Body).Decode(&entity)
	if err != nil {
		sendErrorResponse(w, http.StatusBadRequest, "Invalid request body")
		return
	}

	// Set timestamps
	entity.CreatedAt = time.Now()
	entity.UpdatedAt = time.Now()

	response := Response{
		Message: "Data created successfully",
		Data:    entity,
		Status:  201,
	}
	sendJSONResponse(w, http.StatusCreated, response)
}

// Helper function to send JSON responses
func sendJSONResponse(w http.ResponseWriter, statusCode int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	json.NewEncoder(w).Encode(data)
}

// Helper function to send error responses
func sendErrorResponse(w http.ResponseWriter, statusCode int, message string) {
	response := Response{
		Message: message,
		Status:  statusCode,
	}
	sendJSONResponse(w, statusCode, response)
}

// Middleware for logging requests
func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		log.Printf("Started %s %s", r.Method, r.URL.Path)
		next.ServeHTTP(w, r)
		log.Printf("Completed in %v", time.Since(start))
	})
}

func main() {
	router := mux.NewRouter()

	// Apply middleware
	router.Use(loggingMiddleware)

	// Define routes
	router.HandleFunc("/", homeHandler).Methods("GET")
	router.HandleFunc("/health", healthHandler).Methods("GET")
	router.HandleFunc("/api/data", getDataHandler).Methods("GET")
	router.HandleFunc("/api/data", createDataHandler).Methods("POST")

	// Start server
	port := ":8080"
	log.Printf("Server starting on port %s", port)
	if err := http.ListenAndServe(port, router); err != nil {
		log.Fatal(err)
	}
}
