ENV := dev
# CHANGE if diff product
PRODUCT := <PRODUCT>
# CHANGE stackname. This is the lambda name	
STACKNAME := <STACKNAME>
# CHANGE service.
SERVICE := <SERVICE>
# CHANGE s3 bucket if needed.
S3BUCKET := <S3BUCKET>

validate:
	sam validate
bootstrap:
# 	pip3 install pytest --user
	pip3 install -r file-api/src/requirements.txt

upload-swagger:
	aws s3 cp swagger.yaml s3://<api-bucket>/swagger/
pack:
	sam validate
	rm -rf ./build
# 	cd vx-authorizer && sh tests/test_runner.sh
	sam build --use-container --build-dir ./build
	cd ./build && rm -rf ${FileApi}/*dist-info*
	cd ./build && sam package --output-template-file deploy.yaml --s3-bucket $(S3BUCKET) --s3-prefix <s3-prefix>
	cd ..
test-authorizer:
	 sh tests/test_runner.sh
test-cache-reader:
	echo "Write me some tests!!!"
deploy:
	aws cloudformation deploy --template-file ./build/deploy.yaml --stack-name $(ENV)-$(PRODUCT)-$(STACKNAME) --capabilities CAPABILITY_IAM --parameter-overrides $(shell cat app.properties) Alias=canary Stage=dev
delete:
	aws cloudformation delete-stack --stack-name $(ENV)-$(PRODUCT)-$(STACKNAME)
