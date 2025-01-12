FROM public.ecr.aws/lambda/python:3.11

#COPY requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT} 

RUN pip install -r requirements.txt

#Copy everything in gradescrape
COPY gradescrape/* ${LAMBDA_TASK_ROOT}

#Copy token
COPY token.json ${LAMBDA_TASK_ROOT}

CMD ["scrapy", "crawl", "gradespider"]