# Update
sudo yum update -y

# Install Anaconda
wget https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh
bash Anaconda3-5.1.0-Linux-x86_64.sh -b

# Change default path
echo 'export PATH="/home/ec2-user/anaconda3/bin:$PATH"' >> ~/.bashrc
. ~/.bashrc

# Install required packages
pip install pymongo sodapy
