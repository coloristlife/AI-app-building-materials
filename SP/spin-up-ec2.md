Account: corp-ess-nonprod (130312249203)


ADFS-MHF-PowerUser

## necessary Tags for EC2

Owner	yani.dong@spglobal.com  
APPID	CloudSecurityPOc  
MaintenanceWindow	Thu-22:00-UTC  
Environment	POC  

## AMI 

https://github.com/spglobal-innersource/dts-corp-pe-image-release

GPU:

US-east-1
ami-0ad95ae7696452886
"LINUX2023-ECS-GPU": [
      {
        "current": {
          "ap-northeast-1": "ami-0d70df371be26e8ac",
          "ap-northeast-2": "ami-0583d47f873b0e796",
          "ap-south-1": "ami-0465fe2a73a5622df",
          "ap-southeast-1": "ami-06af8eaf54b4a91bf",
          "ap-southeast-2": "ami-0bfa6e93f7a200ced",
          "ap-southeast-4": "ami-0a2c44ea42f064359",
          "ca-central-1": "ami-076292e2afa12258b",
          "eu-central-1": "ami-0281d3e2eb3ecf257",
          "eu-west-1": "ami-0afb8f4c32942499b",
          "eu-west-2": "ami-03e05bbcbd3770c60",
          "me-central-1": "ami-0e33e428d0ad68184",
          "us-east-1": "ami-0ad95ae7696452886",
          "us-east-2": "ami-04f3e29d52841fc97",
          "us-west-2": "ami-0850e132c73f7e286"
        }
      },

2. 如果你想使用 GPU，应该换成哪种实例？
在 AWS 上，只有以 G, P, 或 L 开头的实例才带有 GPU。针对你目前的 Qwen3-4B 扫描任务，以下是性价比最高的推荐：
实例类型	GPU 型号	显存	建议场景
g4dn.xlarge	NVIDIA T4	16GB	首选推荐。运行 4B-7B 模型速度飞快，且价格最便宜。
g5.xlarge	NVIDIA A10G	24GB	性能更强。如果你想跑 14B 以上的大模型，选这个。
p3.2xlarge	NVIDIA V100	16GB	较老但依然强力，适合深度学习计算。

CPU:
ami-0e7d084d6a66a62d7 

Red Hat Enterprise Linux

name : Encrypted_SPGi-RHEL10-2026-07-04

## other configurations


IAM role : edx-ec2-role

IMDSv2 : Required   (i.e. Metadata version V2 only)

Termination protection: Enabled

Enable public IP



## VPC
VPC: vpc-02030dede905ccd1e  
subnet : subnet-00387c657dd6554aa  
subnet-00387c657dd6554aa (project-subnet-public1-us-east-1a)

sg: yani-sg


route table for VPC

----
## troubleshoot a lack of internet connectivity on your Amazon EC2 instance


To troubleshoot a lack of internet connectivity on your Amazon EC2 instance while trying to install Ollama, you must verify your AWS networking layers step-by-step. Outbound internet access is required both for the installation script (`curl -fsSL https://ollama.com/install.sh | sh`) and for downloading models (`ollama pull`).

### 1. Determine Your Subnet Type
The first step is to identify if your EC2 instance is in a **Public Subnet** or a **Private Subnet**.

*   **Public Subnet:** Direct access via an Internet Gateway.
*   **Private Subnet:** Indirect access via a NAT Gateway or NAT Instance.

### 2. Troubleshooting Public Subnets
If your instance is in a public subnet, check these three requirements:
*   **Public IP Address:** Ensure the EC2 instance has a **Public IPv4 address** or an **Elastic IP** assigned. An instance in a public subnet cannot reach the internet without one, as the Internet Gateway needs a public address to translate traffic.
*   **Internet Gateway (IGW):** Confirm an IGW is created and attached to your VPC.
*   **Route Table:** Check the route table associated with the subnet. It must have a route for `0.0.0.0/0` with the **Target** set to your Internet Gateway ID (e.g., `igw-xxxxxxxx`).

### 3. Troubleshooting Private Subnets
If your instance is in a private subnet, it does not have a public IP and relies on a NAT Gateway.
*   **NAT Gateway:** Ensure a NAT Gateway exists in a **different, public subnet** within the same VPC.
*   **Route Table:** The private subnet’s route table must have a route for `0.0.0.0/0` with the **Target** set to the NAT Gateway ID (e.g., `nat-xxxxxxxx`).
*   **Public Subnet Route:** Ensure the public subnet containing the NAT Gateway itself has a route to an Internet Gateway.

### 4. Check Security Groups & NACLs
Even if routing is correct, "firewall" rules may be blocking traffic.
*   **Security Group Outbound Rules:** By default, EC2 security groups allow all outbound traffic. If you have restricted these, ensure there is a rule allowing **HTTPS (Port 443)** and **HTTP (Port 80)** to `0.0.0.0/0` so the instance can reach the Ollama installation and model registry.
*   **Network ACLs (NACLs):** Check the NACLs for the subnet. Unlike Security Groups, NACLs are stateless. You must allow:
    *   **Outbound:** Port 80 and 443 to `0.0.0.0/0`.
    *   **Inbound:** **Ephemeral ports** (typically 1024–65535) to allow return traffic from the internet.

### 5. OS-Level Verification
If the AWS infrastructure is correct, check the instance's internal configuration:
*   **DNS Resolution:** Run `ping google.com` or `nslookup ollama.com`. If it fails but `ping 8.8.8.8` works, your instance cannot reach a DNS server. Ensure **DNS Resolution** and **DNS Hostnames** are enabled in your VPC settings.
*   **Proxy Settings:** If your company uses a proxy, you may need to export proxy variables before running the install script:
    ```bash
    export http_proxy=http://your-proxy-ip:port
    export https_proxy=http://your-proxy-ip:port
    ```
*   **Test Connectivity:** Use `curl -I https://ollama.com` to see if you get a response. If it hangs, the issue is almost certainly a missing route or security group rule.

### Summary Checklist
| Component | Requirement |
| :--- | :--- |
| **Instance IP** | Must have Public IP (for Public Subnet) |
| **Route Table** | `0.0.0.0/0` -> `igw-xxx` OR `nat-xxx` |
| **Security Group** | Outbound Rule: Port 443 (HTTPS) allowed |
| **NAT Gateway** | Must be in a Public Subnet with its own IGW route |
| **DNS Settings** | VPC must have "DNS Resolution" enabled |


-----

### can't create NAT gateway 
Action Blocked: ec2:CreateNatGateway
Policy ID: DenyNATGatewayCreation
Why it triggered:
The policy contains an Explicit Deny. In AWS, a "Deny" always overrides any "Allow" permissions you might have.
The policy specifically targets the action you are trying to perform (ec2:CreateNatGateway).
Your specific identity (yani.dong@spglobal.com) is matched in the policy's principal list.

所以选择VPC   vpc-e946008d  自带NAT gateway， 但是route table 没有使用NAT Gateway