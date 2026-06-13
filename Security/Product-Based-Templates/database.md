
# Encryption at Rest
Is the PostgreSQL database encrypted at rest? What encryption mechanism is used (e.g., AWS RDS encryption, Transparent Data Encryption)?

Database breach exposing certificate data, extracted metadata, user information


---
Is Elasticsearch data encrypted at rest if sensitive data stored?
risk: Search index exposure containing sensitive extracted data


----
How are messages in ActiveMQ secured? Is message-level encryption implemented for queued processing jobs?
risk: Queue poisoning, exposure of document metadata in transit


Are database queries parameterized to prevent SQL injection attacks
risk: Database compromise, data exfiltration


Is there row-level security or multi-tenancy enforcement in database PostgreSQL to isolate data 
risk: Cross-tenant data access


Are database backups encrypted and stored securely? How frequently are backups performed?
risk: Backup theft, data loss


Is there a disaster recovery plan for PostgreSQL? What is the RTO/RPO?
risk: Extended downtime, data loss in catastrophic failure


Are database audit logs enabled to track all data access and modifications?
risk: Undetected unauthorized database access