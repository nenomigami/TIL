# Mysql Backup and Load databases

환경변수 C:\Program Files\MariaDB 10.5\bin 등록

### 모든 데이터 베이스 백업
mysqldump --all-databases -u [사용자 계정] -p --default-character-set=euckr > [백업된 DB].sql
```mysql
mysqldump --all-databases -uroot -p --default-character-set=euckr > all.sql
passowrd : 123456
```
### 모든 데이터 베이스 복원
mysql --all-databases -u [사용자 계정] -p < [백업된 DB].sql
```mysql
mysql -uroot -p < all.sql
passowrd : 123456
```

### 특정 데이터베이스 백업
mysqldump -u [사용자 계정] -p [패스워드] [원본 데이터베이스명] > [생성할 백업 DB명].sql
```mysql
mysqldump -u test_user -p test_db > backup_test_db.sql
passowrd : 123456
```

### 특정 데이터베이스 복원
mysql -u [사용자 계정] -p [패스워드] [복원할 DB] < [백업된 DB].sql
```mysql
mysql -u test_user -p test_db < backup_test_db.sql
passowrd : 123456
```

### 특정 테이블 백업
mysqldump -u [사용자 계정] -p [패스워드] [데이터베이스명] [원본 백업받을 테이블명] > [백업받을 테이블명].sql
```mysql
mysqldump -u test_user -p test_db test_table > backup_test_table.sql
passowrd : 123456
```

### 특정 테이블 복원
 mysql -u [사용자 계정] -p [패스워드] [복원할 DB ] < [백업된 테이블].sql
```mysql
mysql -u test_user -p 123456 test_db < backup_test_table.sql
passowrd : 123456
```
