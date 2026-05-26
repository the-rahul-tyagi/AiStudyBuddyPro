output "ec2_public_ip" {
  description = "Public IP of EC2 instance"
  value       = aws_instance.ai_study_buddy_ec2.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS of EC2 instance"
  value       = aws_instance.ai_study_buddy_ec2.public_dns
}