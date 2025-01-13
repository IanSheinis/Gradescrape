# Use AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11

# Copy the requirements.txt and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

# Copy the gradescrape directory into the Lambda task root
COPY gradescrape ${LAMBDA_TASK_ROOT}/gradescrape

# Set the Python path to include the task root
ENV PYTHONPATH=${LAMBDA_TASK_ROOT}

#Copy the lambda function into the Lambda task root
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

WORKDIR ${LAMBDA_TASK_ROOT}
# Set the handler function for AWS Lambda
CMD ["lambda_function.lambda_handler"]
