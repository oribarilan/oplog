# Logging Libraries

## Why oplog?

oplog is a minimal and modern logging library for Python applications, which offers a different paradigm for logging, which is based on the concept of logging operations. Instead of creating a "log-book", which is a long scroll of text messages, oplog is about logging operations with rich structured data. This allows you to query, analyze and monitor your app in a modern and performant way.
oplog focuses on simple and minimal API, and is built on top of the standard Python logging library - to make it easy to integrate and use, even for existing projects.

## Not sure oplog is for you? There are alternatives!

oplog is not alone. There are some other great logging libraries out there that you can consider.

All content below is my own personal impression and opinion, which is meant to provide some guidance on picking the right logging library for you. It is not meant to be a comprehensive review of the libraries, nor a critic.
Please try them out yourself and see what works best for your project.

| Library                                       | Loggin Paradigm      | API          | Promise                | Migration | Feature-set  |
| --------------------------------------------- | -------------------- | ------------ | ---------------------- | --------- | ------------ |
| [oplog](https://github.com/oribarilan/oplog)   | Operation-based + Key-Value    | Standard     | Clean Code + Structure | Easy      | Working on it 🤓 |
| [loguru](https://github.com/Delgan/loguru)     | Message-based       | Custom       | API Minimality         | Hard      | Very Rich    |
| [structlog](https://github.com/hynek/structlog)| Message-based + Key-Value | Custom       | Structure              | Med       | Rich         |
| [logbook](https://github.com/getlogbook/logbook)| Message-based      | Standard-ish | Performance            | Hard      | Ok           |
