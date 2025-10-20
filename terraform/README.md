# Terraform Infrastructure

This directory contains Terraform configuration for provisioning AWS infrastructure for the Django-PostgreSQL application.

## Architecture

The infrastructure consists of:
- **VPC** with public subnet and internet gateway
- **4 EC2 instances** (t2.micro, free-tier eligible):
  - Controller: Terraform, Ansible, CI/CD tools
  - Swarm Manager: Docker Swarm manager node
  - Swarm Worker A: Docker Swarm worker node
  - Swarm Worker B: Docker Swarm worker node
- **Elastic IPs** for all instances (static public IPs)
- **Security Group** with required ports for HTTP, SSH, Docker Swarm
- **SSH Key Pair** (auto-generated)

## Files

- `main.tf`: Main infrastructure configuration
- `variables.tf`: Input variables
- `outputs.tf`: Output values
- `terraform.tfvars.example`: Example variables file
- `user-data/`: Instance initialization scripts
- `terraform-key.pem`: Generated SSH private key (created after apply)

## Prerequisites

1. **AWS CLI configured** with appropriate credentials:
   ```bash
   aws configure
   ```

2. **Terraform installed** (version >= 1.0):
   ```bash
   # On Ubuntu/Debian
   wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
   echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
   sudo apt update && sudo apt install terraform
   ```

3. **AWS permissions** for the following services:
   - EC2 (instances, security groups, key pairs)
   - VPC (VPC, subnets, internet gateway, route tables)
   - Elastic IPs

## Quick Start

1. **Copy and customize variables:**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your preferred values
   ```

2. **Initialize Terraform:**
   ```bash
   terraform init
   ```

3. **Plan the deployment:**
   ```bash
   terraform plan
   ```

4. **Apply the configuration:**
   ```bash
   terraform apply
   ```

5. **Get the outputs:**
   ```bash
   terraform output
   ```

## Configuration

### Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `aws_region` | AWS region | `us-east-1` |
| `project_name` | Project name | `devops-assignment` |
| `environment` | Environment name | `dev` |
| `instance_type` | EC2 instance type | `t2.micro` |
| `vpc_cidr` | VPC CIDR block | `10.0.0.0/16` |
| `public_subnet_cidr` | Public subnet CIDR | `10.0.1.0/24` |
| `allowed_ssh_cidr` | SSH access CIDR | `0.0.0.0/0` |

### Security Groups

The security group allows:
- **SSH (22)**: From anywhere (configurable)
- **HTTP (80)**: From anywhere
- **HTTPS (443)**: From anywhere
- **Django (8000)**: From anywhere
- **Docker Swarm (2377, 7946, 4789)**: Within VPC
- **PostgreSQL (5432)**: Within VPC

## Outputs

After successful deployment, you'll get:
- Public and private IP addresses for all instances
- Instance IDs
- VPC and subnet information
- SSH key pair details
- Path to the generated private key file

## SSH Access

The private key is automatically generated and saved as `terraform-key.pem`:

```bash
# SSH to controller
ssh -i terraform-key.pem ubuntu@<controller_public_ip>

# SSH to swarm manager
ssh -i terraform-key.pem ubuntu@<manager_public_ip>

# SSH to workers
ssh -i terraform-key.pem ubuntu@<worker_a_public_ip>
ssh -i terraform-key.pem ubuntu@<worker_b_public_ip>
```

## Instance Roles

### Controller
- Terraform and Ansible installed
- Docker for building images
- Jenkins for CI/CD
- Git and development tools
- SSH key for Ansible automation

### Swarm Nodes (Manager + Workers)
- Docker and Docker Compose installed
- Configured for Docker Swarm
- Firewall rules for Swarm communication
- Monitoring tools (htop, iotop, nethogs)

## Cost Considerations

- All instances use `t2.micro` (free tier eligible)
- Elastic IPs are free when attached to running instances
- Data transfer charges may apply
- Stop instances when not in use to avoid charges

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

**Warning**: This will permanently delete all AWS resources created by this configuration.

## Troubleshooting

### Common Issues

1. **AWS credentials not configured:**
   ```bash
   aws configure
   # or set environment variables:
   export AWS_ACCESS_KEY_ID="your-access-key"
   export AWS_SECRET_ACCESS_KEY="your-secret-key"
   ```

2. **Insufficient permissions:**
   Ensure your AWS user has permissions for EC2, VPC, and related services.

3. **Instance limits:**
   Check your AWS account limits for EC2 instances in the chosen region.

4. **SSH connection issues:**
   - Ensure the private key has correct permissions: `chmod 600 terraform-key.pem`
   - Check security group rules
   - Verify the instance is running

### Useful Commands

```bash
# Check Terraform state
terraform state list

# Show specific resource
terraform state show aws_instance.controller

# Import existing resource (if needed)
terraform import aws_instance.controller i-1234567890abcdef0

# Refresh state
terraform refresh

# Format configuration files
terraform fmt

# Validate configuration
terraform validate
```

## Integration with Ansible

The Terraform outputs are designed to work with Ansible inventory:

```bash
# Generate Ansible inventory from Terraform outputs
terraform output -json > terraform-outputs.json
```

The Ansible configuration will use these outputs to configure the infrastructure automatically.