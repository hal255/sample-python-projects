import cv2
import configparser
import pyglet
import os

from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

class VideoPlayer():
  def __init__(self) -> None:
    self.config = None
    self.media_sources = []

  def setup_config(self):
    self.config = configparser.ConfigParser()
    self.config.read('config.properties')

  def play_video_cv2(self, video_filename=None):
    if not video_filename:
      video_filename = self.config['VideoSection']['sample_video']
      if not video_filename:
        print("Error getting video")
        return False

    my_video = cv2.VideoCapture(video_filename)

    while True:
      ret, frame = my_video.read()
      # TODO: change name of window from output to be more dynamic
      cv2.imshow('output', frame)

      # note: needs '&' in if statement, the usual 'and' does not work
      if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
    my_video.release()
    cv2.destroyAllWindows()

  def play_video_pyglet(self, video_filename=None):
    if not video_filename:
      video_filename = self.config['VideoSection']['sample_video']
      if not video_filename:
        print("Error getting video")
        return False

    # video path
    vidPath = video_filename
    
    # creating a source object
    source = pyglet.media.StreamingSource()
    
    # load the media from the source
    MediaLoad = pyglet.media.load(vidPath)
    video_format = MediaLoad.video_format
    multiplier = 1
    aspect_ratio = int(video_format.sample_aspect * multiplier)

    # width of window
    width = video_format.width * aspect_ratio
    center_w = int(video_format.width/multiplier)
      
    # height of window
    height = video_format.height * aspect_ratio
    center_h = int(video_format.height/multiplier)
      
    # caption i.e title of the window
    title = "VideoOutput"

    # creating a window
    window = pyglet.window.Window(width, height, title)
    # window = pyglet.window.Window(fullscreen=True)
    
    # creating a media player object
    player = pyglet.media.Player()
    
    # add this media in the queue
    player.queue(MediaLoad)
    
    # play the video
    player.play()
    
    # on draw event
    @window.event
    def on_draw():
        
      # clea the window
      window.clear()
      
      # if player source exist
      # and video format exist
      if player.source and player.source.video_format:
          
        # get the texture of video and
        # make surface to display on the screen
        player.get_texture().blit(center_w, center_h)
            
            
    # key press event    
    @window.event
    def on_key_press(symbol, modifier):
      
      # key "p" get press
      if symbol == pyglet.window.key.P:
          
        # printing the message
        print("Key : P is pressed")
        
        # pause the video
        if player.playing:
          player.pause()
          
          # printing message
          print("Video is paused")
          
          
      # key "r" get press
      if symbol == pyglet.window.key.R:
          
        # printing the message
        print("Key : R is pressed")
        
        # resume the video
        if not player.playing:
          player.play()
        
          # printing message
          print("Video is resumed")
    
    # run the pyglet application
    pyglet.app.run()

  def play_video_moviepy(self, video_filename=None):
    if not video_filename:
      video_filename = self.config['VideoSection']['sample_video']
      if not video_filename:
        print("Error getting video")
        return False

    with VideoFileClip(video_filename) as video:
      audio = video.audio
      duration = video.duration # == audio.duration, presented in seconds, float
      #note video.fps != audio.fps
      step = 0.1
      for t in range(int(duration / step)): # runs through audio/video frames obtaining them by timestamp with step 100 msec
        t = t * step
        if t > audio.duration or t > video.duration: break
        audio_frame = audio.get_frame(t) #numpy array representing mono/stereo values
        video_frame = video.get_frame(t) #numpy array representing RGB/gray frame
        video.show(t)
  
  def get_video_parts(self, video_filename=None, start_time=0, end_time=0, steps_num=1):
    if not video_filename:
      video_filename = self.config['VideoSection']['sample_video']
      output_video_location = self.config['VideoSection']['video_output']
    if not video_filename:
      print("Error getting video")
      return False
    
    base_name_ext = os.path.basename(video_filename)
    base_name = base_name_ext.split('.')[0]

    if not output_video_location:
      print("Error finding output location")
      output_video_location = 'test_video_'
    
    output_video_name = f'{output_video_location}{base_name}'
      
    with VideoFileClip(video_filename) as video:
      audio = video.audio
      max_duration = video.duration if video.duration < audio.duration else audio.duration
      if start_time >= max_duration:
        print('Video Editor: start_time exceeds max video duration')
        return
      end_time = max_duration if max_duration <= end_time else end_time
      targetname = f'{output_video_name}{start_time}_to_{end_time}.mp4'
      ffmpeg_extract_subclip(video_filename, start_time, end_time, targetname=targetname)

  def play_videos_group(self):
    test_video_path = self.config['VideoSection']['video_output']
    if not test_video_path:
      print("Error getting videos")
      return False

    # creating a source object
    source = pyglet.media.StreamingSource()
    
    # caption i.e title of the window
    title = "VideoOutput"

    
    # creating a media player object
    player = pyglet.media.Player()
 
    for filename in os.listdir(test_video_path):
      video_filename = f'{test_video_path}{filename}'
    
      # load the media from the source
      MediaLoad = pyglet.media.load(video_filename)
      video_format = MediaLoad.video_format
      if not video_format:
        print('Error: video editor, playing video groups, can not read file')
        continue

      # width of window
      width = 320 if not video_format else video_format.width
        
      # height of window
      height = 640 if not video_format else video_format.height
        
      # creating a window
      window = pyglet.window.Window(width, height, title)
      # window = pyglet.window.Window(fullscreen=True)
    
      # add this media in the queue
      player.queue(MediaLoad)
    
    # play the video
    player.play()
    
    # on draw event
    @window.event
    def on_draw():
        
      # clea the window
      window.clear()
      
      # if player source exist
      # and video format exist
      if player.source and player.source.video_format:
          
        # get the texture of video and
        # make surface to display on the screen
        player.get_texture().blit(0, 0)
            
            
    # key press event    
    @window.event
    def on_key_press(symbol, modifier):
      
      # key "p" get press
      if symbol == pyglet.window.key.P:
          
        # printing the message
        print("Key : P is pressed")
        
        # pause the video
        if player.playing:
          player.pause()
          
          # printing message
          print("Video is paused")
          
      # key "r" get press
      if symbol == pyglet.window.key.R:
          
        # printing the message
        print("Key : R is pressed")
        
        # resume the video
        if not player.playing:
          player.play()
        
          # printing message
          print("Video is resumed")
    
      # key "q" get press
      if symbol == pyglet.window.key.Q:
          
        # printing the message
        print("Key : Q is pressed")
        
        # resume the video
        if player.playing:
          pyglet.app.exit()
        
          # printing message
          print("Video is ending")

    # run the pyglet application
    pyglet.app.run()



  def generate_test_videos(self):
    i = 3
    start_time = 0
    end_time = 0
    while i >= 0:
      start_time = end_time
      end_time += 5
      self.get_video_parts(start_time=start_time, end_time=end_time)
      i -= 1
    print('video_player: done')


if __name__ == '__main__':
  vplayer = VideoPlayer()
  vplayer.setup_config()
  # vplayer.generate_test_videos()
  # vplayer.play_video_pyglet()
  # vplayer.play_video_cv2()
  # vplayer.play_video_moviepy()

  vplayer.play_videos_group()

