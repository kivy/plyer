#import <Foundation/Foundation.h>
#import <Security/Security.h>

@interface KeychainBridge : NSObject

+ (BOOL)saveWithService:(NSString *)service account:(NSString *)account value:(NSString *)value;
+ (NSString *)retrieveWithService:(NSString *)service account:(NSString *)account;
+ (BOOL)deleteWithService:(NSString *)service account:(NSString *)account;

@end

@implementation KeychainBridge

+ (BOOL)saveWithService:(NSString *)service account:(NSString *)account value:(NSString *)value {
    NSDictionary *query = @{
        (__bridge id)kSecClass: (__bridge id)kSecClassGenericPassword,
        (__bridge id)kSecAttrService: service,
        (__bridge id)kSecAttrAccount: account,
        (__bridge id)kSecValueData: [value dataUsingEncoding:NSUTF8StringEncoding]
    };

    OSStatus status = SecItemAdd((__bridge CFDictionaryRef)query, NULL);
    return status == errSecSuccess;
}

+ (NSString *)retrieveWithService:(NSString *)service account:(NSString *)account {
    NSDictionary *query = @{
        (__bridge id)kSecClass: (__bridge id)kSecClassGenericPassword,
        (__bridge id)kSecAttrService: service,
        (__bridge id)kSecAttrAccount: account,
        (__bridge id)kSecReturnData: (__bridge id)kCFBooleanTrue,
        (__bridge id)kSecMatchLimit: (__bridge id)kSecMatchLimitOne
    };

    CFDataRef result = NULL;
    SecItemCopyMatching((__bridge CFDictionaryRef)query, (CFTypeRef *)&result);

    if (result) {
        NSString *value = [[NSString alloc] initWithData:(__bridge NSData *)result encoding:NSUTF8StringEncoding];
        return value;
    }

    return nil;
}

+ (BOOL)deleteWithService:(NSString *)service account:(NSString *)account {
    NSDictionary *query = @{
        (__bridge id)kSecClass: (__bridge id)kSecClassGenericPassword,
        (__bridge id)kSecAttrService: service,
        (__bridge id)kSecAttrAccount: account
    };

    OSStatus status = SecItemDelete((__bridge CFDictionaryRef)query);
    return status == errSecSuccess;
}

@end
