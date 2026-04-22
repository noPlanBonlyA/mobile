/*  src/components/Schedule.jsx
    Виджет расписания с кнопками для преподавателя     */

import React, { useRef,useState,useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import '../styles/Schedule.css';
import '../styles/ManageUserPage.css'; // Фирменные стили кнопок
import api from '../api/axiosInstance';
import { getUserScheduleOptimized, updateLessonGroup } from '../services/scheduleService';
import { createLessonCoinsHistory } from '../services/coinHistoryService';

// === accent color (как в SchedulePage) ===
const PALETTE = [
  '#3B82F6', '#10B981', '#F59E0B', '#EF4444',
  '#8B5CF6', '#06B6D4', '#A855F7', '#22C55E',
  '#E11D48', '#14B8A6'
];
function hashCode(str=''){ let h=0; for (let i=0;i<String(str).length;i++){ h=(h<<5)-h+String(str).charCodeAt(i); h|=0;} return Math.abs(h); }
function pickColorFromKey(key){ if(!key) return '#00B18F'; return PALETTE[ hashCode(String(key)) % PALETTE.length ]; }
function hexToRGBA(hex, a=0.10){
  const v=hex.replace('#','');
  const r=parseInt(v.length===3?v[0]+v[0]:v.slice(0,2),16);
  const g=parseInt(v.length===3?v[1]+v[1]:v.slice(2,4),16);
  const b=parseInt(v.length===3?v[2]+v[2]:v.slice(4,6),16);
  return `rgba(${r},${g},${b},${a})`;
}
function keyForAccent(ev){
  return ev?.group_id || ev?.group_name || ev?.course_id || ev?.course_name || 'default';
}

export default function Schedule({ events, onSelect, selectedEvent, onClose, onCardClick }) {
  
  const { user } = useAuth();
  const navigate = useNavigate();
  const scrollerRef = useRef(null);

  useEffect(() => {
    const el = scrollerRef.current;
    if (!el) return;
    const update = () => {
      const gutter = el.offsetWidth - el.clientWidth; // ширина скроллбара
      el.style.setProperty('--sbw', `${gutter}px`);
    };
    update();
    window.addEventListener('resize', update);
    return () => window.removeEventListener('resize', update);
  }, []);
  // Логируем структуру событий для отладки
  console.log('[Schedule] Component received events:', events);
  if (events && events.length > 0) {
    console.log('[Schedule] First event structure:', events[0]);
    console.log('[Schedule] First event course_id:', events[0].course_id);
    console.log('[Schedule] First event lesson_id:', events[0].lesson_id);
    console.log('[Schedule] Event keys:', Object.keys(events[0]));
  }
  
  // Логируем selectedEvent при изменении
  console.log('[Schedule] selectedEvent:', selectedEvent);
  if (selectedEvent) {
    console.log('[Schedule] selectedEvent course_id:', selectedEvent.course_id);
    console.log('[Schedule] selectedEvent lesson_id:', selectedEvent.lesson_id);
  }
  
  const [conductingLesson, setConductingLesson] = useState(null);
  const [students, setStudents] = useState([]);
  const [loadingStudents, setLoadingStudents] = useState(false);
  const [studentGrades, setStudentGrades] = useState({});
  const [studentComments, setStudentComments] = useState({});
  const [homeworkData, setHomeworkData] = useState({ 
    name: '', 
    file: null, 
    textContent: '' 
  });
  const [uploadingHomework, setUploadingHomework] = useState(false);
  const [toggleLoading, setToggleLoading] = useState(false);
  
  // Состояния для редактирования времени урока
  const [editingTime, setEditingTime] = useState(null);
  const [timeFormData, setTimeFormData] = useState({
    start_datetime: '',
    end_datetime: '',
    auditorium: ''
  });
  const [savingTime, setSavingTime] = useState(false);
// Лочим вертикальный скролл страницы, когда открыт виджет/модалка
useEffect(() => {
  const needLock = Boolean(selectedEvent || conductingLesson || editingTime);
  const body = document.body;

  if (!needLock) return;

  const prev = {
    overflow: body.style.overflow
  };

  body.style.overflow = 'hidden';

  return () => {
    body.style.overflow = prev.overflow;
  };
}, [selectedEvent, conductingLesson, editingTime]);

  if (!events || events.length === 0) {
    return (
      <div className="schedule-empty">
        <div className="empty-icon">📅</div>
        <p>На этот день занятий нет</p>
        <span className="empty-subtitle">Отдыхайте или повторяйте материал</span>
      </div>
    );
  }

  const formatTime = (dateString) => {
    if (!dateString) return '—';
    return new Date(dateString).toLocaleTimeString('ru-RU', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatDate = (dateString) => {
    if (!dateString) return '—';
    return new Date(dateString).toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit'
    });
  };


  const formatTimeRange = (ev) => {
  const s = ev.start_datetime || ev.start;
  const e = ev.end_datetime || ev.end;
  const from = formatTime(s);
  const to = formatTime(e);
  
  // Всегда показываем и начало, и конец времени с тире
  if (from !== '—' && to !== '—') {
    return `${from} — ${to}`;
  } else if (from !== '—') {
    return `${from} — ...`; // Показываем тире даже если конец неизвестен
  } else {
    return '—';
  }
};

// NEW: бейдж типа занятия ("Практика" / "Мероприятие")
const getLessonBadge = (ev) => {
  const raw = (ev.lesson_type || ev.type || ev.type_name || '').toString().trim().toLowerCase();
  const isEvent = getEventType(ev) === 'event' || raw === 'event';
  return {
    text: isEvent ? 'Меро' : 'Урок',
    isEvent
  };
};


  const getTimeUntil = (dateString) => {
    if (!dateString) return '';
    const now = new Date();
    const lessonTime = new Date(dateString);
    const diffMs = lessonTime - now;
    
    if (diffMs < 0) return 'Прошло';
    
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
    
    if (diffHours > 0) {
      return `через ${diffHours}ч ${diffMinutes}м`;
    } else if (diffMinutes > 0) {
      return `через ${diffMinutes}м`;
    } else {
      return 'сейчас';
    }
  };

  const getStatusClass = (event) => {
    // Определяем тип события
    const isEvent = !event.lesson_id && event.event_id;
    const baseClass = isEvent ? 'event-item' : '';
    
    if (event.is_opened) return `opened ${baseClass}`;
    const now = new Date();
    const lessonTime = new Date(event.start_datetime || event.start);
    return `${now < lessonTime ? 'scheduled' : 'closed'} ${baseClass}`;
  };
  
  const getStatusText = (event) => {
    if (event.is_opened) return 'Открыт';
    const now = new Date();
    const lessonTime = new Date(event.start_datetime || event.start);
    return now < lessonTime ? 'Запланирован' : 'Закрыт';
  };

  // Функция для определения типа события
  const getEventType = (event) => {
    return !event.lesson_id && event.event_id ? 'event' : 'lesson';
  };

  const getEventDisplayName = (event) => {
    if (getEventType(event) === 'event') {
      return event.name || event.event_name || event.lesson_name || 'Мероприятие без названия';
    }
    return event.lesson_name || 'Урок';
  };

  const getEventSubtitle = (event) => {
    if (getEventType(event) === 'event') {
      return event.description || 'Мероприятие';
    }
    return event.course_name || 'Курс';
  };

  // НОВОЕ: Функция для открытия/закрытия урока
  const handleToggleLessonAccess = async (event) => {
    try {
      setToggleLoading(true);
      
      // ДЕБАГ: Проверяем структуру event
      console.log('[Schedule] DEBUG - Full event object:', event);
      console.log('[Schedule] DEBUG - User role:', user.role);
      console.log('[Schedule] DEBUG - Event fields:', {
        id: event.id,
        lesson_id: event.lesson_id,
        group_id: event.group_id,
        start_datetime: event.start_datetime,
        end_datetime: event.end_datetime,
        is_opened: event.is_opened,
        auditorium: event.auditorium
      });
      
      // Проверяем права пользователя
      if (user.role !== 'teacher' && user.role !== 'admin' && user.role !== 'superadmin') {
        alert('У вас нет прав для изменения доступа к уроку');
        return;
      }
      
      // Проверяем наличие обязательных полей
      if (!event.id || !event.lesson_id || !event.group_id) {
        console.error('[Schedule] Missing required fields:', {
          id: event.id,
          lesson_id: event.lesson_id,
          group_id: event.group_id
        });
        alert('Не хватает данных для обновления урока');
        return;
      }
      
      const newOpenedState = !event.is_opened;
      
      // Формируем payload с проверкой типов
      const updatePayload = {
        lesson_id: String(event.lesson_id),
        group_id: String(event.group_id),
        start_datetime: event.start_datetime || new Date().toISOString(),
        end_datetime: event.end_datetime || new Date().toISOString(),
        is_opened: Boolean(newOpenedState),
        auditorium: String(event.auditorium || ""),
        id: String(event.id)
      };
      
      console.log('[Schedule] DEBUG - Update payload:', updatePayload);
      console.log('[Schedule] DEBUG - API endpoint:', `/courses/lesson-group/${event.id}`);
      
      // Обновляем lesson-group через API
      const response = await api.put(`/courses/lesson-group/${event.id}`, updatePayload);
      
      console.log('[Schedule] Lesson access toggled successfully:', response.data);
      
      alert(newOpenedState ? 'Урок открыт для студентов!' : 'Урок закрыт для студентов');
      
      // Перезагружаем страницу для обновления данных
      window.location.reload();
      
    } catch (error) {
      console.error('[Schedule] Error toggling lesson access:', error);
      console.error('[Schedule] Error response:', error.response);
      console.error('[Schedule] Error data:', error.response?.data);
      
      // Детальная обработка ошибок
      if (error.response?.status === 403) {
        alert('У вас нет прав для изменения доступа к уроку. Возможные причины:\n- Вы не являетесь преподавателем этого урока\n- У вас недостаточно прав в системе');
      } else if (error.response?.status === 404) {
        alert('Урок не найден или был удален');
      } else if (error.response?.status === 422) {
        alert('Неверные данные для обновления урока. Проверьте консоль для деталей.');
        console.error('[Schedule] Validation details:', error.response?.data?.detail);
      } else {
        const errorMessage = error.response?.data?.detail || 
                            error.response?.data?.message || 
                            'Ошибка изменения доступа к уроку';
        alert(`Ошибка: ${errorMessage}`);
      }
    } finally {
      setToggleLoading(false);
    }
  };

  // Функция для загрузки студентов урока
  const loadLessonStudents = async (lessonGroupId) => {
    try {
      setLoadingStudents(true);
      console.log('[Schedule] Loading students for lesson group:', lessonGroupId);
      
      const response = await api.get('/courses/lesson-student', {
        params: { lesson_group_id: lessonGroupId }
      });
      
      console.log('[Schedule] Students loaded:', response.data);
      setStudents(response.data || []);
      
      // Инициализируем состояния оценок и комментариев
      const initialGrades = {};
      const initialComments = {};
      
      response.data.forEach(student => {
        initialGrades[student.id] = {
          coins_for_visit: student.coins_for_visit || 0,
          grade_for_visit: student.grade_for_visit || 0,
          is_visited: student.is_visited || false,
          is_excused_absence: student.is_excused_absence || false
        };
        initialComments[student.id] = '';
      });
      
      setStudentGrades(initialGrades);
      setStudentComments(initialComments);
      
    } catch (error) {
      console.error('[Schedule] Error loading students:', error);
      alert('Ошибка загрузки списка студентов');
    } finally {
      setLoadingStudents(false);
    }
  };

  // Обработчик "Провести урок"
  const handleConductLesson = async (event) => {
    console.log('[Schedule] Conducting lesson:', event);
    console.log('[Schedule] Event course_id:', event.course_id);
    console.log('[Schedule] Event lesson_id:', event.lesson_id);
    
    // Если course_id отсутствует, пытаемся получить его из полного расписания
    let courseId = event.course_id;
    
    if (!courseId && event.lesson_id) {
      try {
        console.log('[Schedule] Course ID missing, trying to get from full schedule...');
        const scheduleResponse = await api.get('/schedule/');
        const scheduleData = scheduleResponse.data;
        
        // Ищем событие в полном расписании по ID или lesson_id + group_id
        const matchingEvent = scheduleData.find(item => 
          item.id === event.id || 
          (item.lesson_id === event.lesson_id && item.group_id === event.group_id)
        );
        
        if (matchingEvent && matchingEvent.course_id) {
          courseId = matchingEvent.course_id;
          console.log('[Schedule] Retrieved course_id from full schedule:', courseId);
        } else {
          console.log('[Schedule] No matching event with course_id found in schedule');
          
          // Попытка 3: Если все еще нет course_id, используем lesson-group API с group_id
          if (event.group_id) {
            try {
              console.log('[Schedule] Trying lesson-group API with group_id parameter...');
              const lessonGroupsResponse = await api.get('/courses/lesson-group', {
                params: { group_id: event.group_id }
              });
              const lessonGroups = lessonGroupsResponse.data;
              
              if (Array.isArray(lessonGroups) && lessonGroups.length > 0) {
                // Находим lesson-group с нужным lesson_id
                const targetLessonGroup = lessonGroups.find(lg => lg.lesson_id === event.lesson_id);
                if (targetLessonGroup && targetLessonGroup.lesson && targetLessonGroup.lesson.course_id) {
                  courseId = targetLessonGroup.lesson.course_id;
                  console.log('[Schedule] Retrieved course_id from lesson-group API:', courseId);
                }
              }
            } catch (lgError) {
              console.warn('[Schedule] Could not get course_id from lesson-group API:', lgError);
            }
          }
        }
      } catch (scheduleError) {
        console.error('[Schedule] Error getting course_id from schedule:', scheduleError);
      }
    }
    
    // Проверяем наличие обязательных полей
    if (!courseId || !event.lesson_id) {
      console.error('[Schedule] Missing course_id or lesson_id:', {
        course_id: courseId,
        lesson_id: event.lesson_id,
        originalEvent: event
      });
      alert('Ошибка: не удалось определить курс или урок. Обратитесь к администратору.');
      return;
    }
    
    // Находим lesson_group_id из расписания
    const lessonGroupId = event.id; // ID из расписания - это lesson_group_id
    
    // Обновляем событие с правильным course_id
    const updatedEvent = { ...event, course_id: courseId };
    
    setConductingLesson({ ...updatedEvent, lesson_group_id: lessonGroupId });
    await loadLessonStudents(lessonGroupId);
  };

  // Функция для открытия модального окна редактирования времени
  const handleEditLessonTime = (event) => {
    console.log('[Schedule] Opening time edit modal for event:', event);
    
    // Проверяем права доступа
    if (user.role !== 'admin' && user.role !== 'superadmin') {
      alert('У вас нет прав для изменения времени урока');
      return;
    }
    
    // Форматируем даты для input datetime-local
    const formatDateTimeLocal = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      // Убираем секунды и миллисекунды для корректного отображения в input
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${year}-${month}-${day}T${hours}:${minutes}`;
    };
    
    setTimeFormData({
      start_datetime: formatDateTimeLocal(event.start_datetime),
      end_datetime: formatDateTimeLocal(event.end_datetime),
      auditorium: event.auditorium || ''
    });
    
    setEditingTime(event);
  };

  // Функция для сохранения изменений времени
  const handleSaveLessonTime = async () => {
    if (!editingTime || !timeFormData.start_datetime || !timeFormData.end_datetime) {
      alert('Пожалуйста, заполните все поля времени');
      return;
    }

    try {
      setSavingTime(true);
      
      // Проверяем логику времени
      const startDate = new Date(timeFormData.start_datetime);
      const endDate = new Date(timeFormData.end_datetime);
      
      if (startDate >= endDate) {
        alert('Время начала должно быть раньше времени окончания');
        return;
      }
      
      // Форматируем данные для API
      const updatePayload = {
        lesson_id: String(editingTime.lesson_id),
        group_id: String(editingTime.group_id),
        start_datetime: startDate.toISOString(),
        end_datetime: endDate.toISOString(),
        is_opened: Boolean(editingTime.is_opened),
        auditorium: String(timeFormData.auditorium),
        id: String(editingTime.id)
      };
      
      console.log('[Schedule] Updating lesson time with payload:', updatePayload);
      
      // Обновляем через API
      const response = await api.put(`/courses/lesson-group/${editingTime.id}`, updatePayload);
      
      console.log('[Schedule] Lesson time updated successfully:', response.data);
      
      alert('Время урока успешно изменено!');
      
      // Закрываем модальное окно и перезагружаем страницу
      setEditingTime(null);
      window.location.reload();
      
    } catch (error) {
      console.error('[Schedule] Error updating lesson time:', error);
      
      if (error.response?.status === 403) {
        alert('У вас нет прав для изменения времени этого урока');
      } else if (error.response?.status === 404) {
        alert('Урок не найден или был удален');
      } else if (error.response?.status === 422) {
        alert('Неверные данные для обновления времени урока');
        console.error('[Schedule] Validation details:', error.response?.data?.detail);
      } else {
        const errorMessage = error.response?.data?.detail || 
                            error.response?.data?.message || 
                            'Ошибка обновления времени урока';
        alert(`Ошибка: ${errorMessage}`);
      }
    } finally {
      setSavingTime(false);
    }
  };

  // Обработчик "Перейти к курсу"
  const handleGoToCourse = (event) => {
    console.log('[Schedule] Going to course:', event);
    
    if (event.course_id) {
      if (user.role === 'teacher') {
        // Преподаватель → страница курса преподавателя
        navigate(`/courses/${event.course_id}/teacher`);
      } else if (user.role === 'student') {
        // Студент → страница курса студента
        navigate(`/courses/${event.course_id}/student`);
      } else if (user.role === 'admin' || user.role === 'superadmin') {
        // Админы → открываем урок как раньше
        if (event.lesson_id) {
          navigate(`/courses/${event.course_id}/teacher/lessons/${event.lesson_id}`);
        } else {
          navigate(`/courses/${event.course_id}/teacher`);
        }
      }
    } else {
      alert('Не удалось определить курс для перехода');
    }
  };

  // Сохранение оценок и комментариев
  const handleSaveGrades = async () => {
    try {
      console.log('[Schedule] Saving grades and comments...');
      
      for (const student of students) {
        const grades = studentGrades[student.id];
        const comment = studentComments[student.id];
        
        if (!grades) continue;
        
        // Обновляем данные студента урока
        const updateData = {
          student_id: student.student_id,
          lesson_group_id: student.lesson_group_id,
          is_visited: Boolean(grades.is_visited),
          is_excused_absence: Boolean(grades.is_excused_absence),
          is_compensated_skip: Boolean(student.is_compensated_skip || false),
          coins_for_visit: Number(grades.coins_for_visit) || 0,
          grade_for_visit: Number(grades.grade_for_visit) || 0,
          is_sent_homework: Boolean(student.is_sent_homework),
          is_graded_homework: Boolean(student.is_graded_homework),
          coins_for_homework: Number(student.coins_for_homework) || 0,
          grade_for_homework: Number(student.grade_for_homework) || 0,
          id: student.id
        };
        
        console.log('[Schedule] Updating lesson student with data:', updateData);
        
        const response = await api.put(`/courses/lesson-student/${student.id}`, updateData);
        console.log('[Schedule] Lesson student updated successfully:', response.data);
        
        // Создаем записи в истории поинтов, если начислены монеты
        if ((updateData.coins_for_visit > 0 || updateData.coins_for_homework > 0) && student.student?.user_id) {
          try {
            await createLessonCoinsHistory(
              student.student.user_id,
              {
                coins_for_visit: updateData.coins_for_visit,
                coins_for_homework: updateData.coins_for_homework
              },
              {
                lesson_name: conductingLesson?.lesson_name || 'Урок',
                course_name: conductingLesson?.course_name
              },
              student.student?.id // Передаем ID профиля студента для уведомлений
            );
            console.log('[Schedule] Coins history records created for student:', student.student.user_id);
          } catch (historyError) {
            console.warn('[Schedule] Failed to create coins history:', historyError);
            // Не прерываем основной процесс, просто логируем предупреждение
          }
        }
        
        // Если есть комментарий, отправляем уведомление
        if (comment && comment.trim()) {
          try {
            const studentProfileId = student.student?.id;
            if (studentProfileId) {
              await api.post('/notifications/', 
                { content: `Комментарий к уроку "${conductingLesson.lesson_name}": ${comment.trim()}` },
                { 
                  params: { 
                    recipient_type: 'student', 
                    recipient_id: studentProfileId 
                  } 
                }
              );
            }
          } catch (notifError) {
            console.error('[Schedule] Error sending notification:', notifError);
          }
        }
      }
      
      alert('Данные урока сохранены!');
      setConductingLesson(null);
      setStudents([]);
      
    } catch (error) {
      console.error('[Schedule] Error saving grades:', error);
      
      // Более детальная обработка ошибок
      let errorMessage = 'Ошибка сохранения данных';
      
      if (error.message && error.message.includes('Network Error')) {
        errorMessage = 'Ошибка сети: Проверьте подключение к серверу';
      } else if (error.response?.status === 500) {
        errorMessage = 'Ошибка сервера (500): Проверьте логи backend сервера';
      } else if (error.response?.status === 404) {
        errorMessage = 'Урок или студент не найден (404)';
      } else if (error.response?.status === 422) {
        errorMessage = 'Неверный формат данных (422): Проверьте отправляемые данные';
      } else if (error.response?.data?.message) {
        errorMessage = `Ошибка: ${error.response.data.message}`;
      }
      
      alert(errorMessage);
    }
  };

  // Обработка изменения оценок
  const handleGradeChange = (studentId, field, value) => {
    setStudentGrades(prev => ({
      ...prev,
      [studentId]: {
        ...prev[studentId],
        [field]: value
      }
    }));
  };

  // Обработка загрузки домашнего задания
  const handleHomeworkUpload = async () => {
    if (!homeworkData.name || (!homeworkData.file && !homeworkData.textContent)) {
      alert('Заполните название и выберите файл или введите текстовое задание');
      return;
    }
    
    // Проверяем наличие обязательных данных урока
    if (!conductingLesson.course_id || !conductingLesson.lesson_id) {
      console.error('[Schedule] Missing lesson data for homework upload:', {
        course_id: conductingLesson.course_id,
        lesson_id: conductingLesson.lesson_id,
        conductingLesson
      });
      alert('Ошибка: не удалось определить курс или урок. Попробуйте заново открыть урок.');
      return;
    }
    
    try {
      setUploadingHomework(true);
      console.log('[Schedule] Uploading homework with:', {
        course_id: conductingLesson.course_id,
        lesson_id: conductingLesson.lesson_id,
        name: homeworkData.name,
        hasText: !!homeworkData.textContent,
        hasFile: !!homeworkData.file
      });
      let uploadedSuccessfully = 0;
      let errors = [];

      // 1. Основное ДЗ (текст)
      if (homeworkData.textContent && homeworkData.textContent.trim()) {
        try {
          const textEndpoint = `/courses/${conductingLesson.course_id}/lessons/${conductingLesson.lesson_id}/homework-material-text`;
          console.log('[Schedule] Text homework endpoint:', textEndpoint);
          await api.post(textEndpoint, {
            name: homeworkData.name,
            html_text: homeworkData.textContent.trim()
          });
          uploadedSuccessfully++;
          console.log('[Schedule] Text homework uploaded successfully');
        } catch (error) {
          console.error('[Schedule] Error uploading text homework:', error);
          errors.push('текстовое задание');
        }
      }

      // 2. Дополнительное ДЗ (файл)
      if (homeworkData.file) {
        try {
          const fileEndpoint = `/courses/${conductingLesson.course_id}/lessons/${conductingLesson.lesson_id}/homework-material`;
          console.log('[Schedule] File homework endpoint:', fileEndpoint);
          const formData = new FormData();
          formData.append('homework_material_name', homeworkData.name);
          formData.append('homework_material_file', homeworkData.file);
          await api.post(fileEndpoint, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
          uploadedSuccessfully++;
          console.log('[Schedule] File homework uploaded successfully');
        } catch (error) {
          console.error('[Schedule] Error uploading file homework:', error);
          errors.push('файл');
        }
      }

      // Показываем результат
      if (uploadedSuccessfully > 0 && errors.length === 0) {
        alert('Домашнее задание загружено успешно!');
        setHomeworkData({ name: '', file: null, textContent: '' });
      } else if (uploadedSuccessfully > 0 && errors.length > 0) {
        alert(`Частично загружено. Ошибка загрузки: ${errors.join(', ')}`);
      } else {
        alert(`Ошибка загрузки домашнего задания: ${errors.join(', ')}`);
      }
    } catch (error) {
      console.error('[Schedule] Error uploading homework:', error);
      alert('Общая ошибка загрузки домашнего задания');
    } finally {
      setUploadingHomework(false);
    }
  };

  // Модальное окно проведения урока
  if (conductingLesson) {
    return (
      <div className="modal-overlay conduct-lesson-modal">
        <div className="modal-content large">
          <div className="modal-header">
            <h2>Провести урок: {conductingLesson.lesson_name}</h2>
            <button className="close-modal" onClick={() => setConductingLesson(null)}>×</button>
          </div>
          
          <div className="modal-body">
            {loadingStudents ? (
              <div className="loading-container">
                <div className="loader"></div>
                <p>Загрузка списка студентов...</p>
              </div>
            ) : (
              <div className="conduct-lesson-content">
                {/* Секция домашнего задания */}
                <div className="homework-upload-section">
                  <h3>Загрузить домашнее задание</h3>
                  <div className="homework-form">
                    <input
                      type="text"
                      placeholder="Название домашнего задания"
                      value={homeworkData.name}
                      onChange={(e) => setHomeworkData(prev => ({ ...prev, name: e.target.value }))}
                    />
                    
                    <div className="homework-content-section">
                      <h4>Текстовое задание (опционально):</h4>
                      <textarea
                        placeholder="Введите текст домашнего задания..."
                        value={homeworkData.textContent}
                        onChange={(e) => setHomeworkData(prev => ({ ...prev, textContent: e.target.value }))}
                        rows={4}
                        style={{ width: '100%', marginBottom: '10px' }}
                      />
                    </div>
                    
                    <div className="homework-file-section">
                      <h4>Файл задания (опционально):</h4>
                      <input
                        type="file"
                        onChange={(e) => setHomeworkData(prev => ({ ...prev, file: e.target.files[0] }))}
                        accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png"
                      />
                    </div>
                    
                    <button 
                      onClick={handleHomeworkUpload}
                      disabled={uploadingHomework || !homeworkData.name || (!homeworkData.file && !homeworkData.textContent)}
                      className="btn-secondary"
                    >
                      {uploadingHomework ? 'Загрузка...' : 'Загрузить ДЗ'}
                    </button>
                  </div>
                </div>

                {/* Список студентов */}
                <div className="students-grades-section">
                  <h3>Студенты группы ({students.length})</h3>
                  <div className="students-list">
                    {students.map(student => (
                      <div key={student.id} className="student-grade-item">
                        <div className="student-info">
                          <h4>{student.student?.user?.first_name} {student.student?.user?.surname}</h4>
                        </div>
                        
                        <div className="grade-controls">
                          <label>
                            <input
                              type="checkbox"
                              checked={studentGrades[student.id]?.is_visited || false}
                              onChange={(e) => handleGradeChange(student.id, 'is_visited', e.target.checked)}
                            />
                            Присутствует
                          </label>
                          
                          <label>
                            <input
                              type="checkbox"
                              checked={studentGrades[student.id]?.is_excused_absence || false}
                              onChange={(e) => handleGradeChange(student.id, 'is_excused_absence', e.target.checked)}
                            />
                            Уважительная причина
                          </label>
                          
                          <label>
                            Баллы за посещение:
                            <input
                              type="number"
                              min="0"
                              max="10"
                              value={studentGrades[student.id]?.coins_for_visit ?? ''}
                              onChange={(e) => handleGradeChange(student.id, 'coins_for_visit', e.target.value === '' ? '' : Number(e.target.value))}
                            />
                          </label>
                          
                          <label>
                            Оценка за урок:
                            <input
                              type="number"
                              min="0"
                              max="5"
                              value={studentGrades[student.id]?.grade_for_visit ?? ''}
                              onChange={(e) => handleGradeChange(student.id, 'grade_for_visit', e.target.value === '' ? '' : Number(e.target.value))}
                            />
                          </label>
                          
                          <label>
                            Комментарий:
                            <textarea
                              placeholder="Комментарий студенту (будет отправлен как уведомление)"
                              value={studentComments[student.id] || ''}
                              onChange={(e) => setStudentComments(prev => ({ ...prev, [student.id]: e.target.value }))}
                              rows={2}
                            />
                          </label>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div className="modal-actions">
                  <button onClick={handleSaveGrades} className="btn-primary">
                    Сохранить
                  </button>
                  <button onClick={() => setConductingLesson(null)} className="btn-secondary">
                    Отмена
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Определяем мобильное устройство
  const isMobile = () => {
    return window.innerWidth <= 768;
  };

  // Рендеринг для мобильных устройств с улучшенной структурой
  const renderMobileScheduleItem = (event, index) => {
  const badge = getLessonBadge(event);
  const accent = pickColorFromKey(keyForAccent(event));
  const styleVars = {
    '--item-accent': accent,
    '--item-accent-bg': hexToRGBA(accent, 0.10),
    '--item-accent-border': hexToRGBA(accent, 0.5)
  };

  return (
    <li
      key={event.id || index}
      style={styleVars}
      className={`schedule-item ${getStatusClass(event)} ${getEventType(event) === 'event' ? 'is-event' : 'is-lesson'}`}
      onClick={(e) => { onCardClick?.(e); onSelect?.(event); }}
    >
      {/* верхняя строка: диапазон времени + бейдж */}
      <div className="schedule-top-row">
        <div className="time-range">{formatTimeRange(event)}</div>
        <span className={`lesson-badge ${badge.isEvent ? 'badge--event' : 'badge--practice'}`}>
          {badge.text}
        </span>
      </div>

      {/* название и курс */}
      <div className="schedule-main-info">
        <div className="title">{getEventDisplayName(event)}</div>
        <div className="schedule-course-info">{getEventSubtitle(event)}</div>
      </div>

      {/* детали */}
      <div className="schedule-details">
        {event.teacher_name && (
          <div className="schedule-detail-item">
            <span className="icon">👤</span>
            <span>{event.teacher_name}</span>
          </div>
        )}
        {event.auditorium && (
          <div className="schedule-detail-item">
            <span className="icon">📍</span>
            <span>{event.auditorium}</span>
          </div>
        )}
      </div>
    </li>
  );
};

  // Рендеринг для десктопных устройств (существующий)
  // NEW: десктопная карточка без teacher-действий (ничего лишнего)
const renderDesktopScheduleItem = (event, index) => {
  const badge = getLessonBadge(event);
  const accent = pickColorFromKey(keyForAccent(event));
  const styleVars = {
    '--item-accent': accent,
    '--item-accent-bg': hexToRGBA(accent, 0.10),
    '--item-accent-border': hexToRGBA(accent, 0.5)
  };

  return (
    <div
      key={event.id || index}
      className={`schedule-desktop-item ${getStatusClass(event)} ${getEventType(event) === 'event' ? 'is-event' : 'is-lesson'}`}
      onClick={(e) => { onCardClick?.(e); onSelect?.(event); }}
    >
      <div className="schedule-card desktop" style={styleVars}>
        {/* верхняя строка: диапазон времени + бейдж */}
        <div className="schedule-top-row">
          <div className="time-range">{formatTimeRange(event)}</div>
          <span className={`lesson-badge ${badge.isEvent ? 'badge--event' : 'badge--practice'}`}>
            {badge.text}
          </span>
        </div>

        {/* название и курс */}
        <div className="schedule-main-info">
          <div className="title">{getEventDisplayName(event)}</div>
          <div className="schedule-course-info">{getEventSubtitle(event)}</div>
        </div>

        {/* детали */}
        <div className="schedule-details">
          {event.teacher_name && (
            <div className="schedule-detail-item">
              <span className="icon">👤</span>
              <span>{event.teacher_name}</span>
            </div>
          )}
          {event.auditorium && (
            <div className="schedule-detail-item">
              <span className="icon">📍</span>
              <span>{event.auditorium}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};


 return (
  <div className="schedule-container">
    <div
      ref={scrollerRef}
      className="schedule-scroller"
      role="region"
      aria-label="Список занятий за день"
    >
      {isMobile() ? (
        <ul className="schedule-list">
          {events.map((event, index) => renderMobileScheduleItem(event, index))}
        </ul>
      ) : (
        <div className="schedule-desktop-list">
          {events.map((event, index) => renderDesktopScheduleItem(event, index))}
        </div>
      )}
    </div>
      
      {/* Виджет с подробностями выбранного события */}
      {selectedEvent && (
        <div className="event-details">
          <button className="close-btn" onClick={onClose}>×</button>
          
          <div className="event-header">
            <h2>{selectedEvent.lesson_name}</h2>
            <span className={`status-badge ${getStatusClass(selectedEvent)}`}>
              {getStatusText(selectedEvent)}
            </span>
          </div>

          <div className="event-info">
            <div className="info-item">
              <strong>Курс:</strong>
              <span>{selectedEvent.course_name}</span>
            </div>
            <div className="info-item">
              <strong>Время:</strong>
              <span>
                {formatTime(selectedEvent.start_datetime)} - {formatTime(selectedEvent.end_datetime)}
              </span>
            </div>
            <div className="info-item">
              <strong>Аудитория:</strong>
              <span>{selectedEvent.auditorium || 'Не указана'}</span>
            </div>
            {selectedEvent.group_name && (
              <div className="info-item">
                <strong>Группа:</strong>
                <span>{selectedEvent.group_name}</span>
              </div>
            )}
            {selectedEvent.teacher_name && (
              <div className="info-item">
                <strong>Преподаватель:</strong>
                <span>{selectedEvent.teacher_name}</span>
              </div>
            )}
            <div className="info-item">
              <strong>Статус доступа:</strong>
              <span style={{ color: selectedEvent.is_opened ? '#22c55e' : '#ef4444' }}>
                {selectedEvent.is_opened ? 'Открыт для студентов' : 'Закрыт для студентов'}
              </span>
            </div>
          </div>

          {/* Блок домашних заданий */}
          {(selectedEvent.homework_materials?.length > 0 || selectedEvent.homework_text) && (
            <div className="homework-section">
              <h3 className="section-title">📝 Домашние задания</h3>
              <div className="homework-items">
                {selectedEvent.homework_materials?.map((hw, index) => (
                  <div key={index} className="homework-item">
                    <div className="homework-header">
                      <span className="homework-name">{hw.name}</span>
                      <span className="homework-type">Файл</span>
                    </div>
                    {hw.description && (
                      <div className="homework-description">{hw.description}</div>
                    )}
                  </div>
                ))}
                {selectedEvent.homework_text && (
                  <div className="homework-item">
                    <div className="homework-header">
                      <span className="homework-name">Текстовое задание</span>
                      <span className="homework-type">Текст</span>
                    </div>
                    <div className="homework-description" dangerouslySetInnerHTML={{ __html: selectedEvent.homework_text }} />
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Блок материалов урока */}
          {(selectedEvent.teacher_materials?.length > 0 || selectedEvent.student_materials?.length > 0) && (
            <div className="materials-section">
              <h3 className="section-title">📚 Материалы урока</h3>
              
              {selectedEvent.teacher_materials?.length > 0 && (
                <div className="material-category">
                  <h4 className="material-category-title">👨‍🏫 Материалы преподавателя</h4>
                  <div className="material-items">
                    {selectedEvent.teacher_materials.map((material, index) => (
                      <div key={index} className="material-item">
                        <span className="material-name">{material.name}</span>
                        <span className="material-type">
                          {material.file_url ? '📁 Файл' : '📝 Текст'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {selectedEvent.student_materials?.length > 0 && (
                <div className="material-category">
                  <h4 className="material-category-title">👨‍🎓 Материалы для студентов</h4>
                  <div className="material-items">
                    {selectedEvent.student_materials.map((material, index) => (
                      <div key={index} className="material-item">
                        <span className="material-name">{material.name}</span>
                        <span className="material-type">
                          {material.file_url ? '📁 Файл' : '📝 Текст'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Кнопки действий для преподавателя и администраторов - только для уроков */}
          {(user.role === 'teacher' || user.role === 'admin' || user.role === 'superadmin') && getEventType(selectedEvent) === 'lesson' && (
            <div className="event-actions">
              <button 
                onClick={() => handleGoToCourse(selectedEvent)}
                className="btn-primary"
              >
                {user.role === 'admin' || user.role === 'superadmin' ? '📖 Перейти к уроку' : '📚 Перейти к курсу'}
              </button>
              <button 
                onClick={() => handleToggleLessonAccess(selectedEvent)}
                className="btn-primary"
                disabled={toggleLoading}
                style={{ 
                  backgroundColor: selectedEvent.is_opened ? '#ef4444' : '#22c55e'
                }}
              >
                {toggleLoading ? '⏳' : selectedEvent.is_opened ? '🔒 Закрыть урок' : '🔓 Открыть урок'}
              </button>
              <button 
                onClick={() => handleConductLesson(selectedEvent)}
                className="btn-primary"
              >
                🎯 Провести урок
              </button>
              {/* Кнопка редактирования времени для админов */}
              {(user.role === 'admin' || user.role === 'superadmin') && (
                <button 
                  onClick={() => handleEditLessonTime(selectedEvent)}
                  className="btn-primary"
                  style={{ backgroundColor: '#3b82f6' }}
                >
                  ⏰ Изменить время
                </button>
              )}
            </div>
          )}

          {/* Кнопка для студента - только если урок открыт И это урок (не мероприятие) */}
          {user.role === 'student' && selectedEvent.is_opened && getEventType(selectedEvent) === 'lesson' && (
            <div className="event-actions">
              <button 
                onClick={() => handleGoToCourse(selectedEvent)}
                className="btn-primary"
              >
                📚 Перейти к курсу
              </button>
            </div>
          )}

          {/* Сообщение для студента если урок закрыт */}
          {user.role === 'student' && !selectedEvent.is_opened && getEventType(selectedEvent) === 'lesson' && (
            <div className="event-actions">
              <p style={{ 
                color: '#6b7280', 
                fontStyle: 'italic', 
                textAlign: 'center',
                margin: 0
              }}>
                Урок пока закрыт преподавателем
              </p>
            </div>
          )}

          {/* Информация для мероприятий */}
          {getEventType(selectedEvent) === 'event' && (
            <div className="event-actions">
              <p style={{ 
                color: '#8b5cf6', 
                fontStyle: 'italic', 
                textAlign: 'center',
                margin: 0,
                fontWeight: '500'
              }}>
                🎉 Это мероприятие - никаких дополнительных действий не требуется
              </p>
            </div>
          )}
        </div>
      )}

      {/* Модальное окно редактирования времени урока */}
      {editingTime && (
        <div className="modal-overlay conduct-lesson-modal">
          <div className="modal-content medium">
            <div className="modal-header">
              <h2>⏰ Изменить время урока</h2>
              <div style={{ fontSize: '14px', color: '#666', marginTop: '4px' }}>
                {editingTime.lesson_name} - {editingTime.course_name}
              </div>
              <button className="close-modal" onClick={() => setEditingTime(null)}>×</button>
            </div>
            
            <div className="modal-body">
              <div className="time-edit-form">
                <div className="form-group">
                  <label htmlFor="start_datetime">Время начала</label>
                  <input
                    type="datetime-local"
                    id="start_datetime"
                    value={timeFormData.start_datetime}
                    onChange={(e) => setTimeFormData(prev => ({
                      ...prev,
                      start_datetime: e.target.value
                    }))}
                    className="form-control"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="end_datetime">Время окончания</label>
                  <input
                    type="datetime-local"
                    id="end_datetime"
                    value={timeFormData.end_datetime}
                    onChange={(e) => setTimeFormData(prev => ({
                      ...prev,
                      end_datetime: e.target.value
                    }))}
                    className="form-control"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="auditorium">Аудитория</label>
                  <input
                    type="text"
                    id="auditorium"
                    value={timeFormData.auditorium}
                    onChange={(e) => setTimeFormData(prev => ({
                      ...prev,
                      auditorium: e.target.value
                    }))}
                    placeholder="Введите номер аудитории"
                    className="form-control"
                  />
                </div>

                <div className="form-actions">
                  <button 
                    onClick={handleSaveLessonTime}
                    className="btn-primary"
                    disabled={savingTime}
                  >
                    {savingTime ? '⏳ Сохранение...' : '💾 Сохранить изменения'}
                  </button>
                  <button 
                    onClick={() => setEditingTime(null)}
                    className="btn-secondary"
                    disabled={savingTime}
                  >
                    ❌ Отмена
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
