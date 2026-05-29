import {
  Column,
  CreateDateColumn,
  Entity,
  PrimaryGeneratedColumn,
} from 'typeorm';

@Entity('compilation_history')
export class CompilationHistory {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ name: 'source_code', type: 'text' })
  sourceCode: string;

  @Column({ name: 'target_variability', length: 32 })
  targetVariability: string;

  @Column({ name: 'execution_mode', length: 32 })
  executionMode: string;

  @Column({ length: 16 })
  status: string;

  @Column({ type: 'text', nullable: true })
  output: string | null;

  @Column({ type: 'text', nullable: true })
  error: string | null;

  @CreateDateColumn({ name: 'created_at', type: 'timestamptz' })
  createdAt: Date;
}
