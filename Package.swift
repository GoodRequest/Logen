// swift-tools-version:5.3
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "logen_ios",
    products: [
        .library(
            name: "logen_ios",
            targets: ["logen_ios"]
        )
    ],
    targets: [
        .target(
            name: "logen_ios",
            dependencies: [],
            path: ".",
            exclude: [
                "README.md",
                "credentials.json",
                "logen.py",
                "logen2.py",
                "./res"
            ]
        )
    ]
)
