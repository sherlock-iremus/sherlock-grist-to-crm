SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
source $SCRIPT_DIR/../ENV
ROOT="$(dirname "$SCRIPT_DIR")"
source ./venv/bin/activate

mkdir -p $ROOT/out/ttl/grist/projects/

ROOT=$ROOT sh $ROOT/scripts/user-projects-case.sh $1