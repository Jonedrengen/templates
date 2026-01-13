// Rust Struct Template
//
// Template for creating a Rust struct with common patterns and traits.

use std::fmt;
use std::time::SystemTime;

/// Represents a basic entity with standard Rust patterns
#[derive(Debug, Clone)]
pub struct Entity {
    id: String,
    name: String,
    created_at: SystemTime,
    metadata: std::collections::HashMap<String, String>,
}

impl Entity {
    /// Creates a new Entity instance
    ///
    /// # Arguments
    ///
    /// * `name` - The name of the entity
    ///
    /// # Examples
    ///
    /// ```
    /// let entity = Entity::new("Example Entity".to_string());
    /// ```
    pub fn new(name: String) -> Self {
        Self {
            id: uuid::Uuid::new_v4().to_string(),
            name,
            created_at: SystemTime::now(),
            metadata: std::collections::HashMap::new(),
        }
    }

    /// Gets the ID of the entity
    pub fn id(&self) -> &str {
        &self.id
    }

    /// Gets the name of the entity
    pub fn name(&self) -> &str {
        &self.name
    }

    /// Sets the name of the entity
    pub fn set_name(&mut self, name: String) {
        self.name = name;
    }

    /// Adds metadata to the entity
    pub fn add_metadata(&mut self, key: String, value: String) {
        self.metadata.insert(key, value);
    }

    /// Gets metadata value by key
    pub fn get_metadata(&self, key: &str) -> Option<&String> {
        self.metadata.get(key)
    }

    /// Processes the entity
    ///
    /// # Returns
    ///
    /// Result indicating success or error
    pub fn process(&self) -> Result<String, String> {
        // Processing logic
        Ok(format!("Processed entity: {}", self.name))
    }
}

// Implement Display trait for pretty printing
impl fmt::Display for Entity {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "Entity {{ id: {}, name: {} }}",
            self.id, self.name
        )
    }
}

// Implement Default trait
impl Default for Entity {
    fn default() -> Self {
        Self::new("Unnamed".to_string())
    }
}

// Implement PartialEq for comparison
impl PartialEq for Entity {
    fn eq(&self, other: &Self) -> bool {
        self.id == other.id
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new_entity() {
        let entity = Entity::new("Test".to_string());
        assert_eq!(entity.name(), "Test");
    }

    #[test]
    fn test_metadata() {
        let mut entity = Entity::new("Test".to_string());
        entity.add_metadata("key".to_string(), "value".to_string());
        assert_eq!(entity.get_metadata("key"), Some(&"value".to_string()));
    }
}
