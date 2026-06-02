import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { CompilationHistory } from './history/entities/compilation-history.entity';
import { HealthModule } from './health/health.module';
import { ProcessModule } from './process/process.module';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        type: 'postgres',
        url: config.get<string>(
          'DATABASE_URL',
          'postgresql://minipar:minipar@localhost:5432/minipar',
        ),
        entities: [CompilationHistory],
        synchronize: false,
        retryAttempts: 15,
        retryDelay: 3000,
      }),
    }),
    HealthModule,
    ProcessModule,
  ],
})
export class AppModule {}
