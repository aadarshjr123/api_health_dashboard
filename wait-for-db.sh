#!/bin/sh
set -e

host="$1"
shift

echo "⏳ Waiting for Postgres ($host) to be ready..."

# Keep trying until pg_isready confirms the DB is ready
until pg_isready -h "$host" -p 5432 -U admin > /dev/null 2>&1
do
  echo "❌ Postgres not ready yet... retrying in 2s"
  sleep 2
done

echo "✅ Postgres is ready! Starting FastAPI..."
exec "$@"
