# CI/CD Configuration

This directory contains CI/CD pipeline configurations for automated deployment of the Django-PostgreSQL application.

## Available CI/CD Options

### 1. GitHub Actions (Recommended)
- **File**: `.github/workflows/deploy.yml`
- **Triggers**: Push to main branch or branches starting with "ITA"
- **Features**: Automated testing, building, deployment, and cleanup

### 2. Jenkins Pipeline
- **File**: `ci/Jenkinsfile`
- **Setup**: `ci/jenkins-setup.sh`
- **Features**: Complete pipeline with notifications and performance testing

## GitHub Actions Setup

### Prerequisites
1. GitHub repository with the project code
2. AWS account with appropriate permissions
3. GitHub repository secrets configured

### Required Secrets
Configure these secrets in your GitHub repository settings:

```
AWS_ACCESS_KEY_ID     - Your AWS access key
AWS_SECRET_ACCESS_KEY - Your AWS secret key
```

### Workflow Stages
1. **Test**: Run Django tests and code linting
2. **Build**: Build Docker images
3. **Deploy**: Provision infrastructure and deploy application
4. **Cleanup**: Destroy infrastructure on failure

### Usage
```bash
# Push to main branch or ITA* branch to trigger deployment
git push origin main

# Or push to your roll number branch
git push origin ITA700
```

## Jenkins Setup

### Installation
Run the setup script on your Jenkins server:

```bash
chmod +x ci/jenkins-setup.sh
./ci/jenkins-setup.sh
```

### Manual Configuration
1. **Install Jenkins** (if not using setup script):
   ```bash
   # Ubuntu/Debian
   wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
   sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
   sudo apt-get update
   sudo apt-get install jenkins
   ```

2. **Install required plugins**:
   - Pipeline
   - Git
   - Docker Pipeline
   - AWS Steps
   - Ansible
   - Email Extension
   - GitHub Integration

3. **Configure credentials**:
   - AWS credentials (ID: `aws-credentials`)
   - SSH private key (ID: `terraform-ssh-key`)

4. **Create Pipeline job**:
   - New Item → Pipeline
   - Pipeline script from SCM
   - Git repository URL
   - Script path: `ci/Jenkinsfile`

### GitHub Webhook
Configure webhook in GitHub repository settings:
- URL: `http://your-jenkins-url:8080/github-webhook/`
- Content type: `application/json`
- Events: Push events

## Pipeline Features

### Testing
- Django application tests
- Code linting with flake8
- Docker image security scanning
- Integration tests
- Performance testing

### Deployment
- Infrastructure provisioning with Terraform
- Server configuration with Ansible
- Docker Swarm deployment
- Health checks and validation

### Notifications
- Email notifications on success/failure
- Slack integration (configurable)
- Build status badges

### Security
- Credential management
- Secret scanning
- Container vulnerability scanning
- Infrastructure security checks

## Environment Variables

### GitHub Actions
```yaml
env:
  AWS_REGION: us-east-1
  PROJECT_NAME: devops-assignment
```

### Jenkins
```groovy
environment {
    AWS_REGION = 'us-east-1'
    PROJECT_NAME = 'devops-assignment'
    AWS_CREDENTIALS = credentials('aws-credentials')
}
```

## Branch Strategy

### Main Branch
- Full deployment pipeline
- Production environment
- Automatic cleanup on failure

### Feature Branches (ITA*)
- Full deployment pipeline
- Development environment
- Manual cleanup required

### Pull Requests
- Testing only
- No deployment
- Code quality checks

## Monitoring and Logging

### Build Artifacts
- Test reports
- Performance reports
- Deployment logs
- Infrastructure outputs

### Notifications
- Build status emails
- Slack notifications
- GitHub status checks

## Troubleshooting

### Common Issues

1. **AWS Credentials**:
   ```bash
   # Verify credentials
   aws sts get-caller-identity
   ```

2. **SSH Connectivity**:
   ```bash
   # Check key permissions
   chmod 600 terraform/terraform-key.pem
   ```

3. **Docker Issues**:
   ```bash
   # Check Docker daemon
   sudo systemctl status docker
   ```

### Debug Commands

```bash
# Check pipeline status
curl -u user:token http://jenkins-url:8080/job/job-name/lastBuild/api/json

# View build logs
curl -u user:token http://jenkins-url:8080/job/job-name/lastBuild/consoleText

# Check GitHub Actions
gh run list
gh run view <run-id>
```

## Performance Optimization

### Build Caching
- Docker layer caching
- Terraform state caching
- Ansible fact caching

### Parallel Execution
- Multi-stage builds
- Parallel testing
- Concurrent deployments

### Resource Management
- Build timeouts
- Resource limits
- Cleanup policies

## Security Best Practices

### Secrets Management
- Use encrypted secrets
- Rotate credentials regularly
- Limit secret scope

### Access Control
- Branch protection rules
- Required reviews
- Status checks

### Infrastructure Security
- Least privilege access
- Network security groups
- Encrypted communications

## Integration Examples

### Slack Notifications
```groovy
// In Jenkinsfile
slackSend channel: '#deployments',
          color: 'good',
          message: "Deployment successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
```

### Custom Webhooks
```yaml
# In GitHub Actions
- name: Notify webhook
  run: |
    curl -X POST ${{ secrets.WEBHOOK_URL }} \
         -H "Content-Type: application/json" \
         -d '{"status": "success", "build": "${{ github.run_number }}"}'
```

## Maintenance

### Regular Tasks
- Update pipeline dependencies
- Review and rotate secrets
- Monitor build performance
- Clean up old artifacts

### Backup Strategy
- Pipeline configurations
- Build artifacts
- Credential backups
- Infrastructure state

## Cost Optimization

### AWS Resources
- Use spot instances for testing
- Automatic resource cleanup
- Resource tagging for cost tracking

### Build Optimization
- Efficient Docker images
- Minimal test datasets
- Parallel execution

This CI/CD setup provides a complete automation solution for the DevOps assignment, ensuring reliable and repeatable deployments while maintaining security and performance standards.