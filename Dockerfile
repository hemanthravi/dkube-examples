FROM ocdr/sklearnserver:0.23.2

RUN apt-get install curl unzip -y
RUN \
    curl -k 'https://34.69.66.134:32222/dkube/v2/ext/users/ocdkube/datums/class/model/datum/insurance/version/1628594122873/export' -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc0YmNkZjBmZWJmNDRiOGRhZGQxZWIyOGM2MjhkYWYxIn0.eyJ1c2VybmFtZSI6Im9jZGt1YmUiLCJyb2xlIjoiZGF0YXNjaWVudGlzdCxtbGUscGUsb3BlcmF0b3IiLCJleHAiOjQ4NjgxNzk4MTMsImlhdCI6MTYyODE3OTgxMywiaXNzIjoiREt1YmUifQ.WbdyrdywEEMk7OD6KEyU8C_HVmXStE_gXgKNQfNnGxVmrrCqBHBV9ZNPYg_g7mk8XTbA3mZ2iJ86sFr9DmXk2yNx-8-Na9zL3XkVPf-a6nE-33QGf1PBemg9s-l-PJ7pWrEXOWttUKRJTJ2M9ZEpUAi9AZZ5UfOvVpudga0bh_XbLmvP7TPCnVOk0g0kvBDWIVvaEvEpznO2WcWYFXUVEh80Okx5205lvGuv9ajQLkphbiNdnnGOV6Wr8TG3WIvN1M5e-74Hj13fUZU7Db1SiQfD2qqidrF5VdLqEK2nDP2y60XaynbWf1XiTqtj70-b8u_zUCU9q3yylDbR1TUigg'  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36' -o model.zip

RUN unzip model.zip


