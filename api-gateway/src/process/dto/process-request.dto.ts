import { IsEnum, IsNotEmpty, IsString } from 'class-validator';
import { ExecutionMode } from '../enums/execution-mode.enum';
import { TargetVariability } from '../enums/target-variability.enum';

export class ProcessRequestDto {
  @IsString()
  @IsNotEmpty()
  sourceCode: string;

  @IsEnum(TargetVariability)
  targetVariability: TargetVariability;

  @IsEnum(ExecutionMode)
  executionMode: ExecutionMode;
}
