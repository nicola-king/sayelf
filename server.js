import { createReadStream } from 'node:fs';
import { stat } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { createServer } from 'node:http';

const port = Number(process.env.PORT || 4173);
const root = process.cwd();
const types = {
  '.css': 'text/css; charset=utf-8',
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
};

createServer(async (request, response) => {
  const url = new URL(request.url, `http://${request.headers.host}`);
  const safePath = normalize(url.pathname).replace(/^([/\\])+/, '');
  const filePath = join(root, safePath || 'index.html');

  if (!filePath.startsWith(root)) {
    response.writeHead(403).end('Forbidden');
    return;
  }

  try {
    const file = await stat(filePath);
    if (!file.isFile()) throw new Error('Not a file');
  } catch {
    response.writeHead(404).end('Not found');
    return;
  }

  response.writeHead(200, { 'content-type': types[extname(filePath)] || 'text/plain' });
  createReadStream(filePath).pipe(response);
}).listen(port, () => {
  console.log(`Sayelf conversation app running at http://localhost:${port}`);
});
