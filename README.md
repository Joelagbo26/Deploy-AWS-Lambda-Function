# Dev environment for deploying AWS Lambda Functions via Ansible

## Description

Automated deployment of AWS Lambda function using Ansible. 

### Architecture

![Alt](/resources/AWS-Lambda-Deploy.jpg "Architecture Diagram")

### Definitions

#### What is a AWS Lambda?

AWS Lambda lets you run code without provisioning or managing servers. 

#### What is [Ansible](https://github.com/ansible/ansible)?

Ansible is a radically simple IT automation platform that makes your applications and systems easier to deploy. Avoid writing scripts or custom code to deploy and update your applications, automate in a language that approaches plain English, using SSH, with no agents to install on remote systems.

## Installation requirements

* Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads.html)
* Clone this repo
* Drop in AWS Credentials @ config/.aws/credentials folder. The aws credentials need to have permissions to manage AWS Lambda. For more information on AWS IAM refer [here](http://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)

## Commands

Start:

`$ vagrant up`

This does the following:

* Copies AWS credentials from host to VM
* Installs [Ansible](https://www.ansible.com/)
* Backs up Ansible hosts file and updates with the one that is provided with the repo.
* Gathers SSH public keys by executing ssh-keyscan on localhost.
* Installs python-pip and necessary aws packages.

SSH into the server

`$ vagrant ssh`

### Establish SSH trust

In order to establish password less access to nodes(and host) we need to establish SSH trust. The ssh-addkey.yml playbook uses authorized_key module which will help in configuring ssh password less logins on remote machines. More details  on authorized_key module can be found [here](http://docs.ansible.com/ansible/authorized_key_module.html).

Check to make sure we do not have public RSA key.   
`$ ls -l .ssh/`

We will create a RSA key by the following command

`$ ssh-keygen -t rsa -b 2048`

Check to make sure we have the id_rsa.pub file present as specified in the ssh-addkey.yml playbook.

Run the ansible play book - ssh-addkey.yml with ask pass option to make sure we are deploying the key to all machines- in this case there is only one machine- localhost.

`$ ansible-playbook deploytoLambda/playbooks/ssh-addkey.yml --ask-pass`

Now try the ansible ping module to ping the local server with the ask password option.

`$ ansible all -m ping`

This is should provide the following output.

```
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```
### Deploy Lambda function to AWS lambda using Ansible

 Here we are using python code that will backup and tag an EC2 instance.

 ![Alt](/resources/backup_ec2.jpg "Architecture Diagram")

 cd into src folder and update the file that will be deployed to lambda.

`$ cd deploytoLambda/src`

cd to playbooks directory once lambda function is ready to be deployed.

`$ cd deploytoLambda/playbooks`

Update the following variables with respective values

* LAMBDA_ARN - AWS IAM role with necessary permissions to execute the lambda function
* INSTANCE_ID - The EC2 instance that is being backed up
* INSTANCE_NAME- Name of the EC2 instance that is backed up
* INSTANCE_DESCRIPTION- Description for the image

Run the ansible playbook to deploy Lambda fucntion to AWS Lambda

`$ ansible-playbook deploy-lambda-function.yml`

This does the following: 

* Zips up the python code
* Creates a Lambda function in AWS Lambda.


## Reference
[AWS Lambda](http://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
