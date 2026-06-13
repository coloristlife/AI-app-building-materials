

# security requirements for the priviledged access of vendor
https://docs.cloud.google.com/docs/security/privileged-access-management

Overview of privileged access
Typically, your customer data is only accessed by you and the Google Cloud services that you enable. In some cases, Google personnel might require access to your data to help provide a contracted service (for example, you require support or need to recover from an outage). This type of access is known as privileged access.

Highly-privileged employees who are temporarily granted or acquire elevated permissions pose a higher insider risk. Our approach to privileged access focuses on reducing the number of possible attack vectors. For example, we use the following security controls:

Redundant authentication schemes
Limited data access pathways
Logging and alerting actions across our systems
Regulated permissions
This approach helps us control and detect internal attacks, limit the impact of incidents, and reduce the risk to your data.

The privileged access management strategy in Google Cloud limits the ability of Google personnel to view or modify customer data. In Google Cloud, limits on privileged access are an integral part of how our products are designed to work.

For more information about when Google personnel might access your data, see the Cloud Data Processing Addendum.





Privileged access philosophy
Google's privileged access philosophy uses the following guiding principles:

Access restrictions must be based on roles and multi-party approvals: Google personnel are denied system access by default. When access is granted, it is temporary and is no greater than necessary to perform their role. Access to customer data, critical operations on production systems, and modifications of source code are controlled by manual and automated verification systems. Google personnel can't access customer data without another individual approving the request. Personnel can only access the resources that are necessary to do their jobs and must provide a valid justification to access customer data. For more information, see How Google protects its production services.

Workloads must have end-to-end protection: With encryption in transit, encryption at rest, and Confidential Computing for encryption in use, Google Cloud can provide end-to-end encryption of customer workloads.

Logging and auditing are continuous: Google personnel access to customer data is logged and threat detection systems conduct real-time audits, alerting the security team when log entries match threat indicators. Internal security teams evaluate alerts and logs to identify and investigate anomalous activities, limiting the scope and impact of any incident. For more information about incident response, see Data incident response process.

Access must be transparent and include customer controls: You can use customer-managed encryption keys (CMEK) to manage your own encryption keys and control access to them. In addition, Access Transparency ensures that all privileged access has a business justification that is logged. Access Approval lets you approve or deny access requests by Google personnel to certain datasets.