# Scripts Directory

This directory contains automation scripts for the DevOps assignment project.

## Scripts

### bootstrap.sh
**Main deployment script** - Provisions infrastructure, configures servers, and deploys the application.

```bash
# Full deployment
./scripts/bootstrap.sh

# With CI/CD setup
./scripts/bootstrap.sh --with-cicd
```

**What it does:**
1. Checks prerequisites (Terraform, Ansible, AWS CLI)
2. Provisions AWS infrastructure with Terraform
3. Configures servers with Ansible
4. Deploys Django application to Docker Swarm
5. Optionally sets up CI/CD pipeline
6. Provides access URLs and next steps

### destroy.sh
**Cleanup script** - Destroys all AWS resources and cleans up local files.

```bash
# Full cleanup
./scripts/destroy.sh

# Skip Docker cleanup (if instances are already stopped)
./scripts/destroy.sh --skip-docker-cleanup
```

**What it does:**
1. Confirms destruction with user
2. Removes Docker stacks from Swarm cluster
3. Destroys AWS infrastructure with Terraform
4. Cleans up local files (SSH keys, state files)
5. Resets Ansible inventory to template

### test.sh
**Testing script** - Comprehensive testing of the deployed application.

```bash
./scripts/test.sh
```

**What it tests:**
1. Infrastructure status (Terraform outputs)
2. SSH connectivity to all servers
3. Docker Swarm cluster health
4. Application endpoint accessibility
5. Application functionality (register/login/home)
6. Database connectivity
7. Basic performance metrics
8. Generates detailed test report

## Prerequisites

Before running any scripts, ensure you have:

1. **AWS CLI configured:**
   ```bash
   aws configure
   ```

2. **Terraform installed:**
   ```bash
   # Ubuntu/Debian
   wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
   echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
   sudo apt update && sudo apt install terraform
   ```

3. **Ansible installed:**
   ```bash
   sudo apt update && sudo apt install ansible
   ```

4. **Git configured (for CI/CD):**
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

## Usage Examples

### Complete Deployment
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Run complete deployment
./scripts/bootstrap.sh

# Test the deployment
./scripts/test.sh

# Clean up when done
./scripts/destroy.sh
```

### Development Workflow
```bash
# Deploy infrastructure
./scripts/bootstrap.sh

# Make changes to application
# ... edit Django code ...

# Redeploy just the application
cd ansible
ansible-playbook playbooks/swarm-deploy.yml

# Test changes
cd ..
./scripts/test.sh
```

### Troubleshooting
```bash
# Check infrastructure status
cd terraform
terraform output

# Check server connectivity
cd ansible
ansible all -m ping

# Check Docker Swarm status
ansible swarm_managers -m shell -a "docker node ls"
ansible swarm_managers -m shell -a "docker service ls"

# Check application logs
ansible swarm_managers -m shell -a "docker service logs myapp_web --tail 50"
```

## Script Features

### Error Handling
- All scripts use `set -e` for immediate exit on errors
- Comprehensive error checking and user feedback
- Graceful cleanup on script interruption

### Logging
- Colored output for better readability
- Timestamped log messages
- Different log levels (info, success, warning, error)

### User Interaction
- Confirmation prompts for destructive operations
- Clear progress indicators
- Helpful next steps and usage instructions

### Flexibility
- Optional parameters for different use cases
- Skip options for partial operations
- Environment variable support

## Output Files

Scripts generate various output files:

- `terraform/terraform-key.pem` - SSH private key for server access
- `ansible/inventory/hosts.yml` - Generated Ansible inventory
- `test-report-*.txt` - Test execution reports
- Various Terraform state and log files

## Security Considerations

- SSH keys are automatically generated and secured (600 permissions)
- AWS credentials are never stored in scripts
- Confirmation required for destructive operations
- Temporary files are cleaned up automatically

## Integration with CI/CD

Scripts are designed to work with CI/CD pipelines:

```yaml
# Example GitHub Actions usage
- name: Deploy infrastructure
  run: ./scripts/bootstrap.sh

- name: Run tests
  run: ./scripts/test.sh

- name: Cleanup on failure
  if: failure()
  run: ./scripts/destroy.sh
```

## Customization

Scripts can be customized by:

1. **Environment variables:**
   ```bash
   export AWS_REGION=us-west-2
   export PROJECT_NAME=my-project
   ./scripts/bootstrap.sh
   ```

2. **Terraform variables:**
   ```bash
   # Edit terraform/terraform.tfvars
   aws_region = "us-west-2"
   instance_type = "t3.micro"
   ```

3. **Ansible variables:**
   ```bash
   # Edit ansible playbooks or use extra-vars
   ansible-playbook playbooks/site.yml --extra-vars "docker_compose_version=2.21.0"
   ```

## Troubleshooting Common Issues

### AWS Permissions
```bash
# Check AWS credentials
aws sts get-caller-identity

# Check required permissions
aws iam get-user
```

### SSH Connectivity
```bash
# Check key permissions
chmod 600 terraform/terraform-key.pem

# Test SSH manually
ssh -i terraform/terraform-key.pem ubuntu@<ip_address>
```

### Docker Issues
```bash
# Check Docker status on remote servers
ansible swarm_nodes -m shell -a "systemctl status docker"

# Restart Docker if needed
ansible swarm_nodes -m shell -a "systemctl restart docker" --become
```

### Application Issues
```bash
# Check service logs
ansible swarm_managers -m shell -a "docker service logs myapp_web"

# Check service status
ansible swarm_managers -m shell -a "docker service ps myapp_web"
```