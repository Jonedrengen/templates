/**
 * TypeScript Interface and Type Template
 * 
 * Template for creating TypeScript interfaces, types, and type guards.
 */

// Interface definition
export interface EntityInterface {
  id: string;
  name: string;
  createdAt: Date;
  updatedAt?: Date;
  metadata?: Record<string, any>;
}

// Type alias
export type EntityStatus = 'active' | 'inactive' | 'pending' | 'archived';

// Generic interface
export interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
  timestamp: string;
}

// Extending interfaces
export interface ExtendedEntity extends EntityInterface {
  status: EntityStatus;
  tags: string[];
}

// Type guard
export function isEntityInterface(obj: any): obj is EntityInterface {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.id === 'string' &&
    typeof obj.name === 'string' &&
    obj.createdAt instanceof Date
  );
}

// Utility types
export type PartialEntity = Partial<EntityInterface>;
export type RequiredEntity = Required<EntityInterface>;
export type ReadonlyEntity = Readonly<EntityInterface>;
export type EntityKeys = keyof EntityInterface;

// Function type
export type ProcessorFunction<T, R> = (input: T) => R | Promise<R>;

// Example usage
const entity: EntityInterface = {
  id: '123',
  name: 'Example Entity',
  createdAt: new Date(),
};

const response: ApiResponse<EntityInterface> = {
  data: entity,
  status: 200,
  message: 'Success',
  timestamp: new Date().toISOString(),
};
