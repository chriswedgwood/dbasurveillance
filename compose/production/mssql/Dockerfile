FROM ubuntu:16.04


EXPOSE 1433

# Copy all SQL Server runtime files from build drop into image.

# Run SQL Server process.
CMD [ "/opt/mssql/bin/sqlservr" ]

COPY ./compose/production/mssql/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
