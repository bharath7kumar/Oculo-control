import lib.template_match as tm
import scipy

prev_amplitude = 0

class classify:

    def __init__(self):
        self.vertical_prev_amplitude = 0
        self.horizontal_prev_amplitude = 0
        self.left_flag = 0
        self.right_flag = 0
        self.up_flag = 0
        self.down_flag = 0
        self.status = "centre"
        self.iterator = 0
        self.vertical_signal_stack = []
        self.horizontal_signal_stack = []
        self.cross_corr_tresh = 0.9

        # ASSIGN TEMPLATES

        self.vertical_signal_stack = []
        self.horizontal_signal_stack = []
        self.left_template = 0
        self.right_template = 0
        self.blink_template = 0
        self.up_template = 0
        self.down_template = 0

    def treshold(self, vertical_amplitude, horizontal_amplitude):
        self.upper_thresh_vertical = 50
        self.lower_thresh_vertical = -50
        self.upper_thresh_horizontal = 50
        self.lower_thresh_horizontal = -50
        self.difference_tresh = 30
        
        self.vertical_amplitude = float(vertical_amplitude)
        self.horizontal_amplitude = float(horizontal_amplitude)
        self.vertical_prev_amplitude = self.vertical_prev_amplitude
        self.horizontal_prev_amplitude = self.horizontal_prev_amplitude
        #print(self.horizontal_prev_amplitude)
        self.vertical_difference = self.vertical_amplitude - self.vertical_prev_amplitude        
        self.horizontal_difference = self.horizontal_amplitude - self.horizontal_prev_amplitude        
        self.horizontal_prev_amplitude = self.horizontal_amplitude
        self.vertical_prev_amplitude = self.vertical_amplitude
        #print(self.horizontal_difference, self.horizontal_amplitude, self.horizontal_prev_amplitude)

        if( self.vertical_amplitude > self.upper_thresh_vertical and self.up_flag is 0 ):
            self.up_flag = 1
            
        if( self.vertical_amplitude < self.lower_thresh_vertical and self.down_flag is 0 ):
            self.down_flag = 1
            
        if( self.horizontal_amplitude > self.upper_thresh_horizontal ):
            self.right_flag = 1
            
        elif( self.horizontal_amplitude < self.lower_thresh_horizontal ):
            self.left_flag = 1

        else:
            self.left_flag = 0
            self.right_flag = 0    
            
        #if( self.horizontal_amplitude > self.upper_thresh_horizontal and self.left_flag is 1):
        #    self.left_flag = 0
            
        #if( self.horizontal_amplitude < self.lower_thresh_horizontal and self.right_flag is 1):
        #    self.right_flag = 0
            
        #if(self.vertical_difference > abs(self.difference_tresh)):
        #    self.up_flag = 0
        #    self.down_flag = 0
        #    self.right_flag = 0
        #    self.left_flag = 0
        #    self.status = "center"
        
        if self.left_flag is 1:
            self.status = "left"
        elif self.right_flag is 1:
            self.status = "right"
        elif self.up_flag is 1:
            self.status = "up"
        elif self.down_flag is 1:
            self.status =  "down"
        else:
            self.status = "center"               

        return self.status    

    def template_match_image(self, frame):
        result = tm.match(frame)
        return result

    def template_match(self, vertical_amplitude, horizontal_amplitude, template_size):
        self.vertical_amplitude = vertical_amplitude
        self.horizontal_amplitude = horizontal_amplitude
        self.vertical_signal_stack = self.vertical_signal_stack.append(vertical_amplitude)
        self.horizontal_signal_stack = self.horizontal_signal_stack.append(horizontal_amplitude)

        if self.iterator > template_size:
            self.vertical_signal_stack.pop(0)
            self.horizontal_signal_stack.pop(0)

        self.left_corr = scipy.stats.pearsonr(self.horizontal_signal_stack, self.left_template)
        self.right_corr = scipy.stats.pearsonr(self.horizontal_signal_stack, self.right_template)
        self.up_corr = scipy.stats.pearsonr(self.vertical_signal_stack, self.up_template)
        self.down_corr = scipy.stats.pearsonr(self.vertical_signal_stack, self.down_template)
        self.blink_corr = scipy.stats.pearsonr(self.vertical_signal_stack, self.blink_template)

        if self.left_corr[0] > 0.9:
            self.status = "left"
        if self.right_corr[0] > 0.9:
            self.status = "right"
        if self.up_corr[0] > 0.9:
            self.status = "up"
        if self.down_corr[0] > 0.9:
            self.status = "down"
        if self.blink_corr[0] > 0.9:
            self.status = "blink"

        return self.status    
                        
if __name__ == "__main__":
    classify.treshold(50)
            
