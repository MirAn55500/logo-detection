#!/bin/bash

echo "=== Logo Detection: Download Weights ==="

mkdir -p weights
cd weights

# Установим gdown для скачивания с Google Drive
pip install gdown -q

echo "[1/3] Downloading YOLOv5 weights (best.pt)..."
gdown 1UNpblgptICtQg9h36wC3B4bS6dFFg3QD -O best.pt

echo "[2/3] Downloading ResNet50 weights..."
gdown 1tnkj3c8FjKHct5OqFE8OURVSEgw4EYn5 -O resnet50_feature_extractor.pth

echo "[3/3] Downloading image features..."
gdown 1fPWgLKaQk5-K59eLU0NFIqJmIoCcaOuS -O image_features.pkl

echo ""
echo "=== Готово! Содержимое weights/: ==="
ls -lh

echo ""
echo "Все файлы скачаны:"
echo "  ✓ best.pt"
echo "  ✓ resnet50_feature_extractor.pth"
echo "  ✓ image_features.pkl"