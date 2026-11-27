#!/usr/bin/env bash
# One-command setup of the TrashLocalisation workspace (sim + edgetrash).
# Needs: Ubuntu 22.04, ROS2 Humble, gh logged in (`gh auth login`).
# Safe to re-run: every step skips what is already done. Only the apt step asks for sudo.
set -euo pipefail

REPO=$(cd "$(dirname "$0")/.." && pwd)
WS=${WS:-$HOME/ros2_ws}
VENV=$WS/.venv
# EdgeTrash next to this repo, but never inside $WS/src: colcon would scan its venvs.
case "$REPO" in
  "$WS"/src/*) EDGETRASH_DIR=${EDGETRASH_DIR:-$HOME/EdgeTrash} ;;
  *) EDGETRASH_DIR=${EDGETRASH_DIR:-$(dirname "$REPO")/EdgeTrash} ;;
esac

# Pinned commits. Bump them on purpose, in their own commit.
EDGETRASH_PIN=81b6204ab28feb8f3fb3b975a9e3b9a328916e67  # benchmark-kit: edgetrash lib + models/manifest.yaml
MODEL_RELEASE=models-v1                                  # EdgeTrash release with the ONNX file + SHA256SUMS
SOURCES=(  # url  commit  folder in $WS/src
  "https://github.com/ROBOTIS-GIT/DynamixelSDK.git 59abd67d1f16a199cf0c8608231aee6bb63a57f3 DynamixelSDK"
  "https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git cdee60f7618b9ed2f85f65259c0f96e3f02b1c55 turtlebot3_msgs"
  "https://github.com/ROBOTIS-GIT/turtlebot3.git 90a68bd2e3c61c12966779da89d8eeaec82730e9 turtlebot3"
  "https://github.com/gerald-rocher/Turtlebot3.git cb2a91bc95d5acc4f2676806bf61625068b1f582 Turtlebot3"
)
# The professor's list (his README) + what our packages need.
APT=(
  git build-essential python3-venv python3-colcon-common-extensions
  ros-humble-rmw-cyclonedds-cpp ros-humble-ros-gz
  ros-humble-cartographer ros-humble-cartographer-ros ros-humble-navigation2 ros-humble-nav2-bringup
  ros-humble-vision-msgs
)

say() { printf '\n== %s\n' "$*"; }

[ -f /opt/ros/humble/setup.bash ] || { echo "ROS2 Humble not found: install it first (professor's README)."; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "gh is missing or not logged in: run 'gh auth login' first."; exit 1; }

say "apt packages"
missing=()
for p in "${APT[@]}"; do
  dpkg-query -W -f='${Status}' "$p" 2>/dev/null | grep -q "install ok installed" || missing+=("$p")
done
if [ ${#missing[@]} -gt 0 ]; then
  sudo apt-get update && sudo apt-get install -y "${missing[@]}"
else
  echo "all installed"
fi

say "source repos in $WS/src"
mkdir -p "$WS/src"
for s in "${SOURCES[@]}"; do
  read -r url sha dir <<<"$s"
  [ -d "$WS/src/$dir/.git" ] || git clone -q "$url" "$WS/src/$dir"
  git -C "$WS/src/$dir" cat-file -e "$sha^{commit}" 2>/dev/null || git -C "$WS/src/$dir" fetch -q origin
  git -C "$WS/src/$dir" -c advice.detachedHead=false checkout -q "$sha"
  echo "$dir @ ${sha:0:7}"
done
case "$REPO" in
  "$WS"/src/*) ;;
  *) [ -e "$WS/src/TrashLocalisation" ] || ln -s "$REPO" "$WS/src/TrashLocalisation"
     echo "TrashLocalisation linked from $REPO" ;;
esac

say "EdgeTrash in $EDGETRASH_DIR"
if [ ! -d "$EDGETRASH_DIR/.git" ]; then
  gh repo clone TrashRobotEdge/EdgeTrash "$EDGETRASH_DIR" -- -q
  git -C "$EDGETRASH_DIR" -c advice.detachedHead=false checkout -q "$EDGETRASH_PIN"
elif ! git -C "$EDGETRASH_DIR" merge-base --is-ancestor "$EDGETRASH_PIN" HEAD; then
  echo "WARNING: your EdgeTrash checkout doesn't contain ${EDGETRASH_PIN:0:7}. Left as is (your branch)."
fi

say "Python venv $VENV (system packages visible, so rclpy works)"
[ -d "$VENV" ] || python3 -m venv --system-site-packages "$VENV"
touch "$VENV/COLCON_IGNORE"
"$VENV/bin/pip" install -q pip==26.3  # Ubuntu's pip 22.0.2 can't do editable installs of EdgeTrash (problems.md)
"$VENV/bin/pip" install -q -e "$EDGETRASH_DIR[onnx,dev]"

say "model files ($MODEL_RELEASE)"
gh release download "$MODEL_RELEASE" -R TrashRobotEdge/EdgeTrash -D "$EDGETRASH_DIR/models/files" --skip-existing
(cd "$EDGETRASH_DIR/models/files" && sha256sum -c SHA256SUMS)

say "build (python -m colcon, so our nodes run with the venv's python)"
set +u  # ROS setup scripts read unset variables
source /opt/ros/humble/setup.bash
source "$VENV/bin/activate"
set -u
(cd "$WS" && python -m colcon build --symlink-install)

say "pre-commit hooks"
(cd "$REPO" && "$VENV/bin/pre-commit" install)

say "~/.bashrc"
add_line() {  # pattern line: append line unless a line matching pattern exists
  grep -q -- "$1" ~/.bashrc 2>/dev/null || { echo "$2" >>~/.bashrc; echo "added: $2"; }
}
add_line "/opt/ros/humble/setup.bash" "source /opt/ros/humble/setup.bash"
add_line "RMW_IMPLEMENTATION=" "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp"
add_line "${WS#"$HOME"/}/install/setup.bash" "source $WS/install/setup.bash"
add_line "TURTLEBOT3_MODEL=" "export TURTLEBOT3_MODEL=burger"
add_line "PROJECT_MODEL=" "export PROJECT_MODEL=turtlebot3_burger_oak_d_pro"

say "done. Open a new shell, then see README > Run."
