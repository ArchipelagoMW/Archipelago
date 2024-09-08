namespace Sly1AP
{
    public partial class Form1 : Form
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            outputTextbox = new RichTextBox();
            connectBtn = new Button();
            label1 = new Label();
            hostTextbox = new TextBox();
            slotTextbox = new TextBox();
            label2 = new Label();
            passwordTextbox = new TextBox();
            label3 = new Label();
            timer1 = new System.Windows.Forms.Timer(components);
            button1 = new Button();
            SuspendLayout();
            // 
            // outputTextbox
            // 
            outputTextbox.BackColor = Color.Navy;
            outputTextbox.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            outputTextbox.ForeColor = SystemColors.Control;
            outputTextbox.Location = new Point(13, 15);
            outputTextbox.Name = "outputTextbox";
            outputTextbox.ReadOnly = true;
            outputTextbox.Size = new Size(432, 371);
            outputTextbox.TabIndex = 0;
            outputTextbox.Text = "";
            // 
            // connectBtn
            // 
            connectBtn.Location = new Point(542, 105);
            connectBtn.Name = "connectBtn";
            connectBtn.Size = new Size(158, 23);
            connectBtn.TabIndex = 1;
            connectBtn.Text = "Connect";
            connectBtn.UseVisualStyleBackColor = true;
            connectBtn.Click += connectBtn_Click;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(467, 21);
            label1.Name = "label1";
            label1.Size = new Size(35, 15);
            label1.TabIndex = 2;
            label1.Text = "Host:";
            // 
            // hostTextbox
            // 
            hostTextbox.BackColor = SystemColors.Control;
            hostTextbox.Location = new Point(542, 18);
            hostTextbox.Name = "hostTextbox";
            hostTextbox.Size = new Size(158, 23);
            hostTextbox.TabIndex = 3;
            hostTextbox.Text = "archipelago.gg:";
            // 
            // slotTextbox
            // 
            slotTextbox.Location = new Point(542, 47);
            slotTextbox.Name = "slotTextbox";
            slotTextbox.Size = new Size(158, 23);
            slotTextbox.TabIndex = 5;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(467, 50);
            label2.Name = "label2";
            label2.Size = new Size(30, 15);
            label2.TabIndex = 4;
            label2.Text = "Slot:";
            // 
            // passwordTextbox
            // 
            passwordTextbox.Location = new Point(542, 76);
            passwordTextbox.Name = "passwordTextbox";
            passwordTextbox.Size = new Size(158, 23);
            passwordTextbox.TabIndex = 7;
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(467, 79);
            label3.Name = "label3";
            label3.Size = new Size(60, 15);
            label3.TabIndex = 6;
            label3.Text = "Password:";
            // 
            // button1
            // 
            button1.Location = new Point(0, 0);
            button1.Name = "button1";
            button1.Size = new Size(75, 23);
            button1.TabIndex = 0;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.Black;
            ClientSize = new Size(723, 403);
            Controls.Add(passwordTextbox);
            Controls.Add(label3);
            Controls.Add(slotTextbox);
            Controls.Add(label2);
            Controls.Add(hostTextbox);
            Controls.Add(label1);
            Controls.Add(connectBtn);
            Controls.Add(outputTextbox);
            ForeColor = SystemColors.ControlLight;
            Icon = (Icon)resources.GetObject("$this.Icon");
            Name = "Form1";
            Text = "Sly 1 AP Client";
            ResumeLayout(false);
            PerformLayout();
        }
        #endregion
        private RichTextBox outputTextbox;
        private Button connectBtn;
        private Label label1;
        private TextBox hostTextbox;
        private TextBox slotTextbox;
        private Label label2;
        private TextBox passwordTextbox;
        private Label label3;
        private System.Windows.Forms.Timer timer1;
        private Button button1;
    }
}