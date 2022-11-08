# PHP 소스코드 보안 취약점 패턴 검출
## I. 설치 및 초기 세팅
### 설치
1. web root 또는 web root 보다 상위 dir에서 실행
```bash
composer require --dev vimeo/psalm
```
2. 초기 설정 파일 생성
```bash
./vendor/bin/psalm --init .
```
> ./ 디렉토리에 psalm.xml 파일이 생성 됨

3. 추가 플러그인 설치
```bash
composer require --dev psalm/plugin-laravel
./vendor/bin/psalm-plugin enable psalm/plugin-laravel
```
4. 초기 세팅 예시
```xml
<?xml version="1.0"?>
<psalm
    errorLevel="3"
    resolveFromConfigFile="true"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="https://getpsalm.org/schema/config"
    xsi:schemaLocation="https://getpsalm.org/schema/config vendor/vimeo/psalm/config.xsd"
>
    <projectFiles>
        <directory name="secu_php_static_analysis/simple-php-website"/>
        <ignoreFiles>
            <directory name="vendor"/>
        </ignoreFiles>
    </projectFiles>
<plugins><pluginClass class="Psalm\LaravelPlugin\Plugin"/></plugins></psalm>
```
errorLevel : 탐지 강도 (시큐어코딩 탐지만을 하기 때문에 낮은강도 8로 설정)

탐지 대상 선택
```xml
<projectFiles>
    <directory name="보안 검사 대상 디렉토리"/>
    <ignoreFiles>
        <directory name="vendor"/>
        <directory name="예외 대상 디렉토리"/>
    </ignoreFiles>
</projectFiles>
```

### II. 보안 탐지 
```bash
./vendor/bin/psalm --taint-analysis
```
