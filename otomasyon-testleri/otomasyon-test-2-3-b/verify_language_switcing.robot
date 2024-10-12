*** Settings ***
Library    SeleniumLibrary
Suite Setup    Open Browser To Baykartech
Suite Teardown    Close Browser

*** Variables ***
${URL}    https://www.baykartech.com
@{SUPPORTED_LANGUAGES}    en    /en/    tr    /tr/

*** Test Cases ***
Verify Language Switching
    FOR    ${lang_code}    ${lang_href}    IN    @{SUPPORTED_LANGUAGES}
        Change Language    ${lang_href}
        Validate Page Content    ${lang_code}
    END

*** Keywords ***
Open Browser To Baykartech
    Open Browser    ${URL}    Chrome
    Maximize Browser Window

Change Language
    [Arguments]    ${lang_href}
    Click Element    xpath=//a[@href='${lang_href}']
    Sleep    2s

Validate Page Content
    [Arguments]    ${lang_code}
    ${current_url} =    Get Location
    Should Contain    ${current_url}    ${lang_code}


#######################################################################
##NOTLAR
##1) Kodu çalıştırmak için terminale robot komutunu yazın. --> "robot verify_language_switching.robot"