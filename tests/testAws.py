from cloud_service_providers.AwsCSP import AwsCSP


def main():
    aws_vm = AwsCSP()
    aws_vm.start_vm()


if __name__ == '__main__':
    main()
