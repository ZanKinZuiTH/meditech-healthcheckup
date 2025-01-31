﻿using MediTech.ViewModels;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace MediTech.Views
{
    /// <summary>
    /// Interaction logic for CustomTemplate.xaml
    /// </summary>
    public partial class CustomTemplate : UserControl
    {
        public CustomTemplate(string typeTemplate,string templateValue = "")
        {
            InitializeComponent();
            this.DataContext = new CustomTemplateViewModel(typeTemplate, templateValue);
        }
    }
}
