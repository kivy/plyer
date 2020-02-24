@interface NativeImagePicker : NSObject
@end
@implementation NativeImagePicker

- (NSString*) getFileName:(NSURL *) ns_url {
    // Return the file name without the path or file extention
    NSString *image_name = ns_url.pathComponents.lastObject;
    NSArray *listItems = [image_name componentsSeparatedByString:@"."];
    NSString *ret = listItems[0];
    return ret;
}

- (NSString*) writeToPNG: (NSDictionary *) info {
    /* Given the info frozen dictionary returned by the file picker, convert
     the image selected to a PNG and return the full path. */

    // Get the image name, stripped of path and extention
    NSString *image_name = [self getFileName: info[UIImagePickerControllerImageURL]];

    // Get the png representation of the image
    UIImage *image = info[UIImagePickerControllerOriginalImage];
    NSData *imageData = UIImagePNGRepresentation(image);

    // Generate the final image destination
    NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString *documentsDirectory = [paths objectAtIndex:0];
    NSString *imagePath = [documentsDirectory stringByAppendingPathComponent:[NSString stringWithFormat:@"%@.png", image_name]];

    // Write the image data to the file
    if (![imageData writeToFile:imagePath atomically:NO])
    {
        NSLog(@"Failed to cache image data to disk");
        return @"";
    }
    else
    {
        NSLog(@"the cachedImagedPath is %@",imagePath);
        return imagePath;
    }
}
@end