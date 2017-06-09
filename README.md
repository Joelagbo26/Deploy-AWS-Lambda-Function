# Dev environment for deploying AWS Lambda Functions via Ansible

## Description

Automated deployment of AWS Lambda function using Ansible. 

### Architecture

![Alt](/resources/AWS-ECS-Deploy.jpg "Architecture Diagram")

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

In order to establish password less access to nodes(and host) we need to establish SSH trust. The ssh-addkey.yml playbook will be used to acheive that objective. We are using the authorized_key module here. It is a module, which will help us configure ssh password less logins on remote machines. We tell the authorized_key module, that we want to add an authorized_key to the remote vagrant user, we define where on the management node we should lookup the key file from, then we make sure it exists on the remote machine.

Check to make sure we do not have public RSA key.   
`$ ls -l .ssh/`

We will create a RSA key by the following command

`$ ssh-keygen -t rsa -b 2048`

Check to make sure we have the id_rsa.pub file present as specified in the ssh-addkey.yml playbook.

Run the ansible play book - ssh-addkey.yml with ask pass option to make sure we are deploying the key to all machines- in this case there is only one machine- localhost.

`$ ansible-playbook deploytoECS/playbooks/ssh-addkey.yml --ask-pass`

Now try the ansible ping module to ping the local server with the ask password option.

`$ ansible all -m ping`

This is should provide the following output.

```
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```
### Deploy ECS task and service to AWS ECS cluster

Cd to playbooks directory

`$ cd deploytoECS/playbooks`

Run the ansible playbook to deploy Wordpress website to ECS task and start a service

`$ ansible-playbook deploy-ecs-task\&service.yml`

This does the following: 

* Creates a task definition using wordpress,phpmyadmin and mysql docker images 
* Creates a ECS service in pre existing cluster(update cluster name in deploy-ecs-task&service.yml file in the "set_fact" task).
* If there are no errors, Wordpress should now be accessible at the Public DNS of the Cluster's Container instance. PHP My admin should be available on the same host at 8181. (Port 8181 needs to be made accesible via security group of the EC2 instance.)


## Reference
[AWS Lambda](http://docs.aws.amazon.com/lambda/latest/dg/welcome.html)