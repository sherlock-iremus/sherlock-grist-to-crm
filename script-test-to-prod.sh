export OUTPUT_TTL_ROOT="/Users/amleth/repositories/iremus-sherlock-data-ttl"
ssh tbottini@data-iremus.huma-num.fr "curl -sX POST http://localhost:3030/iremus/update --data-urlencode 'update=DROP GRAPH <http://data-iremus.huma-num.fr/graph/test>'"
ssh tbottini@data-iremus.huma-num.fr "rm /home/tbottini/ttl/test.ttl"
scp $OUTPUT_TTL_ROOT/test.ttl tbottini@data-iremus.huma-num.fr:/home/tbottini/ttl/
ssh tbottini@data-iremus.huma-num.fr "curl -X PUT -H Content-Type:text/turtle -T /home/tbottini/ttl/test.ttl -G http://localhost:3030/iremus/data?graph=http://data-iremus.huma-num.fr/graph/test"
