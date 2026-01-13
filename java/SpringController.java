/*
 * Spring Boot REST Controller Template
 * 
 * Template for creating a REST API controller with Spring Boot.
 * 
 * Dependencies required in pom.xml or build.gradle:
 * - spring-boot-starter-web
 * - spring-boot-starter-validation
 */

package com.example.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;
import java.util.Optional;

/**
 * REST controller for managing entities.
 */
@RestController
@RequestMapping("/api/entities")
@CrossOrigin(origins = "*")
public class EntityController {

    @Autowired
    private EntityService entityService;

    /**
     * Get all entities.
     *
     * @return List of all entities
     */
    @GetMapping
    public ResponseEntity<List<Entity>> getAllEntities() {
        List<Entity> entities = entityService.findAll();
        return ResponseEntity.ok(entities);
    }

    /**
     * Get entity by ID.
     *
     * @param id The entity ID
     * @return The entity if found
     */
    @GetMapping("/{id}")
    public ResponseEntity<Entity> getEntityById(@PathVariable String id) {
        Optional<Entity> entity = entityService.findById(id);
        return entity.map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Create a new entity.
     *
     * @param entity The entity to create
     * @return The created entity
     */
    @PostMapping
    public ResponseEntity<Entity> createEntity(@Valid @RequestBody Entity entity) {
        Entity created = entityService.create(entity);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    /**
     * Update an existing entity.
     *
     * @param id     The entity ID
     * @param entity The updated entity data
     * @return The updated entity
     */
    @PutMapping("/{id}")
    public ResponseEntity<Entity> updateEntity(
            @PathVariable String id,
            @Valid @RequestBody Entity entity) {
        Optional<Entity> updated = entityService.update(id, entity);
        return updated.map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Delete an entity.
     *
     * @param id The entity ID
     * @return No content response
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteEntity(@PathVariable String id) {
        boolean deleted = entityService.delete(id);
        return deleted ? ResponseEntity.noContent().build()
                : ResponseEntity.notFound().build();
    }

    /**
     * Exception handler for validation errors.
     *
     * @param ex The exception
     * @return Error response
     */
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(ValidationException ex) {
        ErrorResponse error = new ErrorResponse(
                HttpStatus.BAD_REQUEST.value(),
                ex.getMessage()
        );
        return ResponseEntity.badRequest().body(error);
    }

    /**
     * Error response model.
     */
    static class ErrorResponse {
        private int status;
        private String message;

        public ErrorResponse(int status, String message) {
            this.status = status;
            this.message = message;
        }

        // Getters and setters omitted for brevity
    }
}
