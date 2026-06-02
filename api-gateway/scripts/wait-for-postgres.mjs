/**
 * Aguarda postgres estar resolvível e aceitando conexões (evita EAI_AGAIN no WSL2).
 */
import dns from 'node:dns/promises';
import net from 'node:net';

const host = process.env.DB_HOST ?? 'postgres';
const port = Number(process.env.DB_PORT ?? 5432);
const maxAttempts = Number(process.env.DB_WAIT_ATTEMPTS ?? 60);
const delayMs = Number(process.env.DB_WAIT_DELAY_MS ?? 2000);

function tryConnect() {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection({ host, port }, () => {
      socket.end();
      resolve();
    });
    socket.on('error', reject);
    socket.setTimeout(5000, () => {
      socket.destroy();
      reject(new Error('timeout'));
    });
  });
}

async function waitForPostgres() {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      await dns.lookup(host);
      await tryConnect();
      console.log(`[wait-for-postgres] ${host}:${port} ready (attempt ${attempt})`);
      return;
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      console.warn(
        `[wait-for-postgres] attempt ${attempt}/${maxAttempts}: ${host}:${port} — ${msg}`,
      );
      await new Promise((r) => setTimeout(r, delayMs));
    }
  }
  console.error(`[wait-for-postgres] gave up after ${maxAttempts} attempts`);
  process.exit(1);
}

await waitForPostgres();
