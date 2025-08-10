import React, { useState, useCallback } from 'react';
import { Loader2, ArrowRight } from 'lucide-react';

import type { FormData } from './types';
import { ENTITY_TYPE_OPTIONS, GENDER_OPTIONS } from './constants';
import FormField from './components/FormField';
import RadioGroup from './components/RadioGroup';
import Button from './components/Button';

const App: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    recipient: { lastName: '', firstName: '', middleName: '', companyName: '' },
    entityType: 'individual',
    gender: 'male',
    date: '',
  });

  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleRecipientChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      recipient: { ...prev.recipient, [name]: value }
    }));
  }, []);

  const handleEntityTypeChange = useCallback((value: 'individual' | 'legal_entity') => {
      setFormData(prev => ({
          ...prev,
          entityType: value,
          recipient: { lastName: '', firstName: '', middleName: '', companyName: '' }
      }));
  }, []);

  const handleGenderChange = useCallback((value: string) => {
    setFormData(prev => ({ ...prev, gender: value }));
  }, []);

  const handleDateChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, date: e.target.value }));
  }, []);

  const handleGenerateJson = async () => {
    setError(null);
    setIsGenerating(true);

    try {
      const dataToExport: any = {
        entityType: formData.entityType,
        date: formData.date || new Date().toLocaleDateString('ru-RU'),
      };

      if (formData.entityType === 'individual') {
          dataToExport.recipient = {
              lastName: formData.recipient.lastName,
              firstName: formData.recipient.firstName,
              middleName: formData.recipient.middleName,
              gender: formData.gender,
          };
      } else {
          dataToExport.recipient = {
              companyName: formData.recipient.companyName,
          };
      }

      // Step 1: Request PDF generation
      const response = await fetch(`${process.env.SERVER_URL}/generate_letter`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToExport),
      });

      if (!response.ok) {
        throw new Error(`Server responded with status ${response.status}`);
      }

      const result = await response.json();
      if (result.status !== 'Success' || !result.message) {
        throw new Error('Invalid server response');
      }

      // Step 2: Fetch the PDF as a blob
      const pdfResponse = await fetch(result.message);
      if (!pdfResponse.ok) {
        throw new Error(`Failed to fetch PDF: ${pdfResponse.status}`);
      }

      const pdfBlob = await pdfResponse.blob();
      const pdfUrl = URL.createObjectURL(pdfBlob);
      const link = document.createElement('a');
      link.href = pdfUrl;
			if (dataToExport.entityType === 'individual') {
		      link.download = dataToExport.recipient["lastName"] + ' благодарственное письмо.pdf';
			}
			else {
		      link.download = dataToExport.recipient["companyName"] + ' благодарственное письмо.pdf';
			}
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(pdfUrl); // Clean up the temporary URL
    } catch (e) {
      console.error(e);
      setError(`Не удалось скачать PDF: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
        <div className="flex-grow max-w-3xl mx-auto p-4 sm:p-6 lg:p-8 w-full">
            <header className="text-center mb-10">
                <div className="flex items-center justify-center gap-3 mb-2">
                    <h1 className="text-4xl font-bold text-gray-800 tracking-tight">Поздравительное письмо от ЛДПР</h1>
                </div>
                <p className="text-lg text-gray-600">Сгенерируйте персональное поздравление легко и просто!</p>
            </header>

            <main className="bg-white p-8 rounded-2xl shadow-lg border border-gray-200">
                <form className="space-y-8">
                    <div>
                        <label className="block text-sm font-medium text-gray-500 mb-2">Тип получателя</label>
                        <RadioGroup name="entityType" options={ENTITY_TYPE_OPTIONS} selectedValue={formData.entityType} onChange={(value) => handleEntityTypeChange(value as 'individual' | 'legal_entity')} />
                    </div>

                    {formData.entityType === 'individual' ? (
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-x-4 gap-y-6">
                            <FormField label="Фамилия" id="recipientLastName" name="lastName" value={formData.recipient.lastName} onChange={handleRecipientChange} placeholder="Петров" />
                            <FormField label="Имя" id="recipientFirstName" name="firstName" value={formData.recipient.firstName} onChange={handleRecipientChange} placeholder="Петр" />
                            <FormField label="Отчество" id="recipientMiddleName" name="middleName" value={formData.recipient.middleName} onChange={handleRecipientChange} placeholder="Петрович" />
                        </div>
                    ) : (
                        <FormField label="Название компании" id="recipientCompanyName" name="companyName" value={formData.recipient.companyName} onChange={handleRecipientChange} placeholder="Завод «Норникель»" />
                    )}

                    {formData.entityType === 'individual' && (
                        <div>
                            <label className="block text-sm font-medium text-gray-500 mb-2">Пол получателя</label>
                            <RadioGroup name="gender" options={GENDER_OPTIONS} selectedValue={formData.gender} onChange={handleGenderChange} />
                        </div>
                    )}
                    
                    <FormField label="Дата" id="date" name="date" type="text" value={formData.date} onChange={handleDateChange} placeholder={new Date().toLocaleDateString('ru-RU')} />

                    <div className="pt-6 text-center">
                        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
                        <Button onClick={handleGenerateJson} زنديغو disabled={isGenerating}>
                            {isGenerating ? 'Генерация...' : 'Сгенерировать письмо'}
                            {isGenerating ? <Loader2 className="animate-spin ml-2" /> : <ArrowRight className="ml-2 h-5 w-5" />}
                        </Button>
                    </div>
                </form>
            </main>
        </div>
    </div>
  );
};

export default App;
