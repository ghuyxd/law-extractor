# """
# Setup script cho Legal Document Processor
# """
# from setuptools import setup, find_packages

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

# setup(
#     name="legal-document-processor",
#     version="1.0.0",
#     author="Legal Document Processing Team",
#     author_email="contact@example.com",
#     description="Hệ thống xử lý và trích xuất thông tin từ văn bản pháp luật Việt Nam",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/example/legal-document-processor",
#     packages=find_packages(),
#     classifiers=[
#         "Development Status :: 4 - Beta",
#         "Intended Audience :: Legal",
#         "Intended Audience :: Developers",
#         "Topic :: Text Processing :: Linguistic",
#         "License :: OSI Approved :: MIT License",
#         "Programming Language :: Python :: 3",
#         "Programming Language :: Python :: 3.8",
#         "Programming Language :: Python :: 3.9",
#         "Programming Language :: Python :: 3.10",
#         "Programming Language :: Python :: 3.11",
#         "Operating System :: OS Independent",
#     ],
#     python_requires=">=3.8",
#     install_requires=[
#         # Không có dependencies bên ngoài, chỉ sử dụng standard library
#     ],
#     entry_points={
#         "console_scripts": [
#             "legal-processor=main:main",
#         ],
#     },
#     include_package_data=True,
#     package_data={
#         "legal_document_processor": ["*.json", "*.yaml"],
#     },
# )