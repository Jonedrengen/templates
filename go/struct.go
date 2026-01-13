package main

import (
	"fmt"
	"time"
)

// Define an interface
type Entity interface {
	GetID() string
	GetName() string
	Process() error
}

// Struct definition
type BasicEntity struct {
	ID        string
	Name      string
	CreatedAt time.Time
	metadata  map[string]interface{}
}

// Constructor function
func NewBasicEntity(id, name string) *BasicEntity {
	return &BasicEntity{
		ID:        id,
		Name:      name,
		CreatedAt: time.Now(),
		metadata:  make(map[string]interface{}),
	}
}

// Method implementation - implements Entity interface
func (e *BasicEntity) GetID() string {
	return e.ID
}

func (e *BasicEntity) GetName() string {
	return e.Name
}

func (e *BasicEntity) Process() error {
	// Processing logic
	fmt.Printf("Processing entity: %s\n", e.Name)
	return nil
}

// Additional methods
func (e *BasicEntity) SetMetadata(key string, value interface{}) {
	e.metadata[key] = value
}

func (e *BasicEntity) GetMetadata(key string) (interface{}, bool) {
	value, exists := e.metadata[key]
	return value, exists
}

// Method with pointer receiver (modifies the struct)
func (e *BasicEntity) UpdateName(newName string) {
	e.Name = newName
}

// Method with value receiver (doesn't modify the struct)
func (e BasicEntity) String() string {
	return fmt.Sprintf("Entity{ID: %s, Name: %s, CreatedAt: %v}",
		e.ID, e.Name, e.CreatedAt)
}

// Example usage
func main() {
	entity := NewBasicEntity("123", "Example Entity")
	fmt.Println(entity)

	entity.SetMetadata("version", "1.0")
	entity.Process()

	if version, ok := entity.GetMetadata("version"); ok {
		fmt.Printf("Version: %v\n", version)
	}
}
