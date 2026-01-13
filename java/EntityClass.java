/*
 * Java Class Template
 * 
 * Template for creating a standard Java class with common patterns.
 */

package com.example;

import java.time.LocalDateTime;
import java.util.Objects;
import java.util.UUID;

/**
 * Represents a basic entity with standard Java patterns.
 */
public class EntityClass {
    // Private fields
    private final String id;
    private String name;
    private final LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    /**
     * Constructor with required fields.
     *
     * @param name The name of the entity
     */
    public EntityClass(String name) {
        this.id = UUID.randomUUID().toString();
        this.name = name;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * Constructor with all fields.
     *
     * @param id   The unique identifier
     * @param name The name of the entity
     */
    public EntityClass(String id, String name) {
        this.id = id;
        this.name = name;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    // Getters
    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    // Setters
    public void setName(String name) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Name cannot be null or empty");
        }
        this.name = name;
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * Business logic method.
     *
     * @param input The input to process
     * @return The processed result
     */
    public String process(String input) {
        // Processing logic
        return "Processed: " + input;
    }

    // equals method
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        EntityClass that = (EntityClass) o;
        return Objects.equals(id, that.id);
    }

    // hashCode method
    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    // toString method
    @Override
    public String toString() {
        return "EntityClass{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                ", createdAt=" + createdAt +
                ", updatedAt=" + updatedAt +
                '}';
    }
}
