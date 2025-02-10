#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>

@interface Voip : NSObject
@property (nonatomic, assign) BOOL callActive;
@property (nonatomic, assign) BOOL hasReceivedFirstPacket;
@property (nonatomic, assign) AVAudioFormat* inputAudioFormat;
@property (nonatomic, assign) AVAudioFormat* outputAudioFormat;
@property (nonatomic, assign) AVAudioPlayerNode* audioPlayerNode;

- (BOOL)requestMicrophonePermission;
- (void)sendClientID:(NSString *)string;
- (void)installTapOnBus:(AVAudioNode *)node bufferSize:(AVAudioFrameCount)bufferSize;
- (void) receiveAudioData;
- (void)connect:(NSString *)address port:(uint16_t)port ssl:(BOOL)ssl tlsVersion:(NSString *)tlsVersion timeout:(int)timeout;
- (BOOL)connected;
- (void)disconnect;
@end
