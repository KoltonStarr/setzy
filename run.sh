if [ "$1" = "pipeline" ]; then
  # Runs the embedding pipeline along with all other services.   
  docker compose --profile pipeline up -d && docker logs -f setzy-pipeline
else
  # Runs everything except the embedding pipeline.  
  docker compose up -d && docker logs -f setzy-agent
fi
