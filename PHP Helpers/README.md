
#### These are helper classes and functions for common php tasks
1-**VerificationBox** is a group of related classes that accomplish the job of verifying a user using email verfication and handles all the database and emailing legwork.

_Read more_: https://medium.com/@omarbuyazeed/easy-verification-with-laravel-and-verifierclass-dc9be7df8868

2-**Helper Functions** are a group of helper functions that accomplish simple task that are often of repetitive nature in my work such as generating a database backed drop-down list, grabbing parent/child related entities from a database (e.g navigation bar links).

3-**ConfigModel** is an extension for Laravel's Eloquent. It's particularly useful when you are dealing with a Model that stores configuration-level information (e.g logo, address, phone number) of a website. It's an abstract class that, just like Laravel's Eloquent, has to be extended by a concrete model.

4-**StoreFile** is a simple class that securely stores files, keeping you away from the low-level work involved in renaming and moving the files. It builds on _Symfony's UploadedFile_ class.
