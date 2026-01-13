/**
 * TypeScript Class Template
 * 
 * Template for creating a TypeScript class with proper typing.
 */

// Interface for constructor options
interface ClassNameOptions {
  id?: string;
  name: string;
  config?: Record<string, any>;
}

// Main class
export class ClassName {
  private readonly id: string;
  private name: string;
  private config: Record<string, any>;
  private createdAt: Date;

  constructor(options: ClassNameOptions) {
    this.id = options.id || this.generateId();
    this.name = options.name;
    this.config = options.config || {};
    this.createdAt = new Date();
  }

  // Getter
  public getId(): string {
    return this.id;
  }

  // Getter and Setter
  public getName(): string {
    return this.name;
  }

  public setName(name: string): void {
    if (!name || name.trim().length === 0) {
      throw new Error('Name cannot be empty');
    }
    this.name = name;
  }

  // Public method
  public async process(input: string): Promise<string> {
    // Async processing logic
    return await this.performOperation(input);
  }

  // Private method
  private async performOperation(input: string): Promise<string> {
    // Implementation
    return `Processed: ${input}`;
  }

  // Static method
  public static create(options: ClassNameOptions): ClassName {
    return new ClassName(options);
  }

  // Private helper method
  private generateId(): string {
    return `id_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  // Method to serialize
  public toJSON(): object {
    return {
      id: this.id,
      name: this.name,
      config: this.config,
      createdAt: this.createdAt.toISOString(),
    };
  }
}

// Example usage
const instance = new ClassName({ name: 'Example' });
console.log(instance.getId());
