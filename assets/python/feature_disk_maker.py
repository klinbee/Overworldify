import json
import os


def generate_placed_feature(y, xz_spread, feature_name):
    """Template for `placed_feature` at set `y_level` w/ set `xz_spread`"""
    return {
        "feature": feature_name,
        "placement": [
            {"type": "minecraft:height_range", "height": {"absolute": int(y)}},
            {
                "type": "minecraft:random_offset",
                "xz_spread": int(xz_spread),
                "y_spread": int(0),
            },
        ],
    }


def generate_placed_features_for_range(
    layer_height, total_range, feature_name, xz_spreads=[0, 8]
):
    """Generates `placed_feature`s from the given whole range; layer_height comes from disk feature (+/-4 blocks)"""
    features = []
    min_y, max_y = total_range

    # Calculate step size to cover the full range efficiently
    step = layer_height

    # Generate features for each xz_spread variant
    for xz_spread in xz_spreads:
        current_height = min_y + step / 2
        while current_height <= max_y:
            feature = generate_placed_feature(
                y=current_height, xz_spread=xz_spread, feature_name=feature_name
            )
            features.append(feature)
            current_height += step

    return features


def save_features_to_files(features, directory="feature_files"):
    """Save each feature to individual JSON files using naming convention xz{0/8}_y{height}."""
    files_created = []
    os.makedirs(directory, exist_ok=True)

    for feature in features:
        xz_spread = feature["placement"][1]["xz_spread"]
        height = feature["placement"][0]["height"]["absolute"]

        filename = f"xz{xz_spread}_y{height}.json"
        filepath = os.path.join(directory, filename)

        with open(filepath, "w") as f:
            json.dump(feature, f, indent=2)

        files_created.append(filename)

    print(f"Generated {len(files_created)} individual feature files:")

    # Group by xz_spread for summary
    xz_0_count = len([f for f in files_created if f.startswith("xz0_")])
    xz_8_count = len([f for f in files_created if f.startswith("xz8_")])

    print(f"  - {xz_0_count} files with xz_spread=0")
    print(f"  - {xz_8_count} files with xz_spread=8")

    return files_created


if __name__ == "__main__":
    custom_features = generate_placed_features_for_range(
        layer_height=8,
        total_range=(-64, 320),
        feature_name="overworldify:water_to_lava",
    )
    save_features_to_files(custom_features)
    print(f"Custom range features: {len(custom_features)}")
