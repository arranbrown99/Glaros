import unittest
import Driver


def main():
    aws_vm = Driver.cloud_service_providers.AwsCSP()
    aws_vm.start_vm()


if __name__ == '__main__':
    main()
