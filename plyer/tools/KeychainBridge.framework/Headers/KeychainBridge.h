#import <Foundation/Foundation.h>

@interface KeychainBridge : NSObject

+ (BOOL)saveWithService:(NSString *)service account:(NSString *)account value:(NSString *)value;
+ (NSString *)retrieveWithService:(NSString *)service account:(NSString *)account;
+ (BOOL)deleteWithService:(NSString *)service account:(NSString *)account;

@end
