install:
	pip install -r requirements.txt

generate:
	python generate.py --nb_images 50

train:
	python train.py

