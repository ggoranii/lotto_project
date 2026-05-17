FROM nginx:alpine

# 기본 설정 파일 삭제
RUN rm /etc/nginx/conf.d/default.conf

# 새로운 설정 파일 복사
COPY nginx.conf /etc/nginx/conf.d/default.conf